# Exact Runtime Requests

Use this loop for confirmation, message signing, opaque choices, ordinary data
replies, OTP, and operation-owned payment approvals. A request is always bound
to one exact remote `sessionId` and `requestId`; never create a sibling request
because a response, link, or waiter output was lost.

## Create

- Use `request_action_confirmation` for one clearly described consequential
  action. Preserve its exact summary and details. Fulfillment authorizes only
  that action; it does not execute it.
- Use `request_message_signature` for one exact wallet `itemRef` and the
  byte-for-byte message. Preserve whitespace. Never request or expose a private
  key, seed, or mnemonic.
- Use `request_choice` once when the user must select one of a few closed-world
  options. Preserve its exact `sessionId`, `requestId`, option order, and opaque
  option IDs. The selection authorizes only which option to continue with; it
  does not execute, book, purchase, approve payment, or prove settlement.
- Native transfer and x402 operations already return their operation-owned
  request UUID. Their payment decision belongs to the MagicPay approval system:
  read and wait on that exact request, and never ask for a chat confirmation or
  turn a plain chat “confirm” into `decide_request`. Never call
  `request_action_confirmation` or any standalone browser approval to replace a
  native approval.

For operation-owned request inspection or recovery, use `get_request` or
`wait_request` with the exact session and routable UUID
`approval.runtimeRequestId`. Preserve the separate stable operation-owned
`approval.requestId`; that identity is not the request-routing UUID. Normal
composed payment waiting stays with the same `runId` and `wait_payment`.

## One choice request, one conversation control

`request_choice` stores one durable request without opening a widget. Prefer
only the adapter-native picker; when available, do not also show `chatMessage`,
a widget, or `request_url`. Without a suitable native picker, use one
`show_session_request` widget or the unchanged `chatMessage` with `request_url`
as the fallback. Other channels share the same request and first durable
result. Normalize source content and follow the full discretionary
choice rules in [choices.md](choices.md). Submit the matched opaque ID, then
wait on those same IDs:

```text
decide_request({
  sessionId,
  requestId,
  decision: 'confirmed',
  selectedChoiceId
})
```

The first durable decision wins. Reconcile any late or transport-ambiguous
result against the same request instead of overwriting it or creating another.

## Present and wait

Report a returned `request_url` in normal conversation when review is needed.
When `otp_available` is true, explicitly tell the user they may send the fresh
six-digit approval OTP in chat for this exact request. When it is false or
absent, do not mention or request an OTP. For non-choice requests, use a
presentation widget only when the user asks to see that exact request.
For non-choice requests, call `wait_request` with the same IDs. Continue bounded
waiting while it is actively pending, respecting the host's cancellation and
tool limits. An aborted wait returns control to the host/user; it is not an
instruction to loop immediately or proof the remote request was canceled. Use
`get_request` to recover that same request or its exact hosted review link.

Approval, confirmation, choice, OTP, and signature creation are authority or
artifacts, not settlement and not proof that the requested external action ran.

## Decide

- Operation-owned payment approvals are decided in the MagicPay approval
  surface. The agent waits for that exact request; a chat response is not the
  authority to submit `confirmed` or `denied`.
- Submit `confirmed` or `denied` only from the user's explicit decision.
- For a generic choice created by `request_choice`, submit `confirmed` with the
  exact `selectedChoiceId` as described above. Never infer or rewrite it.
- A Memory candidate-conflict request also uses the exact opaque
  `selectedChoiceId`, but its decision is `choose_candidate`. Never substitute
  an item ID or infer a candidate from labels.
- Submit `provided` values only for ordinary fields the user safely supplied in
  chat. Passwords, protected payment fields, private keys, seeds, and other
  protected values in an existing collection must use the secure request
  surface, not `decide_request.values`. Standalone explicit saving uses
  `save_memory_item` directly, including protected supplied values; see [memory.md](memory.md).
- For a typed Memory collection, follow [memory.md](memory.md). Saving stays off
  unless the user's reply to that exact request explicitly chooses **Save**.
  The reply may accept the one clearly offered reuse description or provide its
  own; a complete values-only answer means Use once, without another confirmation.
  Submit `save: true` with one typed `saveGroups` entry per explicitly saved
  group, preserving its exact `groupRef`, template version, field mappings,
  `templateKey`, `displayLabel`, and semantic `description`. Omit `entity` only
  for default Me; preserve an already selected non-default entity even when the
  reply does not repeat its name. A new entity needs explicit user identification.
  Report persistence only from the returned `saveOutcome`, and never repeat values.
- A MagicPay approval OTP is intentionally accepted in chat only when the exact
  request says `otp_available: true`. Submit that fresh six-digit OTP only with
  `confirm_request_otp` on the same request; never place it in `values` or reuse
  it. OAuth and third-party OTPs remain outside chat.

On fulfilled, resume only the exact backend continuation. A protected Memory
collection uses the hosted surface and then the original resolver; generic
request reads/waits/claims remain protected-value-free. On denied, expired, failed,
canceled, session stop, or identity mismatch, stop or follow exact returned
recovery. A signing result may contain a signature artifact, never private key
material.

Browser payment approval and waiting belong only to `run_browser_payment` and
`wait_payment`; follow [host-browser-payments.md](host-browser-payments.md).
