# 05 — Async Tool Calling (Inbound & Outbound)

## Implementation stance

This guide uses a non-blocking tool pattern so your server does not freeze
audio relay while external work is running. In current practitioner testing,
realtime models can often keep the conversation flowing around tool use, but
the exact behavior depends on model family, turn timing, and how you manage
responses. Validate before treating uninterrupted speech as guaranteed.

## Async event flow

```
AI decides to call a tool
  => response.output_item.added (type: "function_call")
  => response.function_call_arguments.done   [arguments ready]
  => [your server fires the function -- do NOT await in the message handler]
  => AI continues generating audio
  => [server calls sendToolResult() when function resolves]
  => AI incorporates result into ongoing speech
```

## Server-side handler

```javascript
openaiWs.on("message", async (rawData) => {
  const event = JSON.parse(rawData);

  if (event.type === "response.function_call_arguments.done") {
    const { call_id, name, arguments: argsJson } = event;
    const args = JSON.parse(argsJson);

    // Fire async -- do NOT await here
    handleToolCall(call_id, name, args, session).catch((err) => {
      console.error("Tool error:", name, err.message);
      sendToolResult(openaiWs, call_id, { error: err.message });
    });
  }

  // Audio relay continues uninterrupted
  if (
    (event.type === "response.output_audio.delta" || event.type === "response.audio.delta") &&
    event.delta && session.streamSid
  ) {
    session.twilioWs?.send(JSON.stringify({
      event: "media", streamSid: session.streamSid,
      media: { payload: event.delta },
    }));
  }
});

async function handleToolCall(callId, toolName, args, session) {
  let result;
  switch (toolName) {
    case "lookup_customer":
      result = await db.customers.findByPhone(args.phone); break;
    case "book_appointment":
      result = await calendar.book(args); break;
    case "add_call_note":
      result = await crm.addNote(args.customer_id, args.note, args.outcome); break;
    case "check_availability":
      result = await staff.checkAvailability(args.person_or_dept); break;
    case "take_message":
      result = await messaging.saveMessage(args); break;
    case "transfer_call":
      result = await handleTransferCall(session.callSid, args.destination); break;
    case "warm_transfer":
      result = await handleWarmTransfer(session.callSid, args.agent_number, args.introduction); break;
    case "hang_up":
      result = await twilioClient.calls(session.callSid).update({ status: "completed" }); break;
    default:
      result = { error: "Unknown tool: " + toolName };
  }
  sendToolResult(session.openaiWs, callId, result);
}

function sendToolResult(ws, callId, result) {
  ws.send(JSON.stringify({
    type: "conversation.item.create",
    item: {
      type: "function_call_output",
      call_id: callId,
      output: JSON.stringify(result),
    },
  }));
  // Do not automatically send response.create after every tool result.
  // In some realtime flows that creates duplicate or overlapping audio.
}
```

## Critical: do not blindly send response.create after tool results

In older patterns you might send `response.create` after a tool result to
prompt the model to continue. In many current realtime flows, doing that
unconditionally can produce duplicate or overlapping audio.

Only send `response.create` explicitly when your tested flow actually needs it,
for example:
- The initial greeting trigger
- After a barge-in cancel where you want a fully fresh response
- In server_vad mode where VAD is not auto-triggering responses

## Designing prompts for async tools

Tell the AI what to say while tools are running:

```
When you call a tool, fill the silence naturally. Examples:
- lookup_customer: "Let me pull up your account..."
- book_appointment: "Getting that scheduled for you now..."
- check_availability: "Let me check their schedule..."
- add_call_note: [silent -- do not announce you are saving notes]
Keep filler varied. Never repeat the same phrase twice in a row.
```

## Tool latency targets

| Tool | Target | Notes |
|---|---|---|
| lookup_customer | <500ms | Index by phone number |
| check_availability | <1s | Simple calendar query |
| book_appointment | <2s | Write + confirm |
| add_call_note | <2s | Fire and forget acceptable |
| take_message | <1s | Simple write |
| transfer_call | <3s | Twilio API call |
| warm_transfer | <5s | Two Twilio API calls |

Tools exceeding 3 seconds regularly will cause repetitive-sounding filler.
Optimize those code paths.

## Tool availability by mode

| Tool | IVR | Receptionist | CSR | Outbound |
|---|---|---|---|---|
| lookup_customer | -- | optional | YES | optional |
| check_availability | -- | YES | -- | -- |
| take_message | -- | YES | YES | -- |
| transfer_call | YES | YES | YES | -- |
| warm_transfer | YES | YES | -- | -- |
| book_appointment | -- | -- | YES | YES |
| add_call_note | -- | -- | YES | YES |
| escalate_to_human | -- | -- | YES | -- |
| hang_up | YES | YES | YES | YES |

Load only the tools appropriate for each mode's opening turn. Add more via
a second session.update after the first AI turn completes (see 06-latency-tuning.md).
