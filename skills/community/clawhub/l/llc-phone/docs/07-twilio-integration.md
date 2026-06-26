# 07 — Twilio Integration

## Audio format

Twilio Media Streams use mu-law (PCMU) at 8,000 Hz, mono, 8-bit. Set both
input and output format to `audio/pcmu` in `session.update` to avoid
transcoding.

```json
"audio": {
  "input":  { "format": { "type": "audio/pcmu" } },
  "output": { "format": { "type": "audio/pcmu" } }
}
```

mu-law silence value is `0xFF`, which can be useful when padding chunks.

## TwiML for outbound calls

```javascript
const call = await twilioClient.calls.create({
  from: process.env.TWILIO_PHONE_NUMBER,
  to: prospectNumber,
  twiml: '<Response><Connect><Stream url="wss://' + DOMAIN + '/media-stream?callId=' + callId + '" /></Connect></Response>',
  statusCallback: "https://" + DOMAIN + "/call-status",
  statusCallbackMethod: "POST",
  statusCallbackEvent: ["no-answer", "busy", "failed", "completed"],
});
```

## TwiML for inbound calls

```javascript
// In POST /inbound-webhook response:
res.type("text/xml").send(
  '<Response><Connect><Stream url="wss://' + DOMAIN + '/media-stream?callId=' + CallSid + '" /></Connect></Response>'
);
```

## Edge colocation

Twilio media routing and network path both affect latency. Place your server
close to the expected Twilio edge and caller population where practical, and
verify any SDK- or account-level edge configuration against current Twilio
docs.

Common edge names seen in Twilio docs include `umatilla`, `ashburn`,
`dublin`, `singapore`, `sydney`, `sao-paulo`, and `tokyo`, but re-check the
current list before deployment.

## Answering Machine Detection (AMD) -- outbound

Do not wait for AMD result before connecting the stream if your goal is to
preserve pre-warm or pre-accept behavior. Async AMD is the pattern to test:

```javascript
const call = await twilioClient.calls.create({
  ...
  machineDetection: "DetectMessageEnd",
  asyncAmd: "true",
  asyncAmdStatusCallback: "https://" + DOMAIN + "/amd-result",
  asyncAmdStatusCallbackMethod: "POST",
});
```

## Stream event reference

Events FROM Twilio to your WebSocket:

| Event | When | Key fields |
|---|---|---|
| connected | WS established | protocol, version |
| start | Call answered + stream active | streamSid, accountSid, callSid, customParameters |
| media | Audio chunk (ongoing) | streamSid, track, chunk, timestamp, payload (base64 PCMU) |
| dtmf | Caller pressed key | streamSid, dtmf.digit |
| stop | Call ended | streamSid |

Events FROM your WebSocket TO Twilio:

| Event | Purpose |
|---|---|
| media | Send audio to caller (streamSid, `media.payload` base64 PCMU) |
| mark | Label a point in the audio stream |
| clear | Discard buffered audio, useful on barge-in |

Use `clear` when you need to flush partially buffered AI audio from Twilio's
buffer after interruption or cancellation.

## Buffer overflow (error 31930)

If your server sends audio faster than Twilio can process it, you can hit a
Stream Media Buffer Overflow. If you are flushing a very large pre-generated
buffer, pace it carefully:

```javascript
async function flushGreetingBuffer(session) {
  session.status = "live";
  for (const chunk of session.greetingBuffer) {
    session.twilioWs.send(JSON.stringify({
      event: "media", streamSid: session.streamSid,
      media: { payload: chunk },
    }));
    // Only needed for very large buffers (>3s of audio):
    // await new Promise(r => setImmediate(r));
  }
  session.greetingBuffer = [];
}
```

## SIP native (future path)

OpenAI's SIP support may eventually reduce the need for a Twilio media bridge
in some architectures. Treat it as a separate design path to evaluate rather
than an automatic replacement.
