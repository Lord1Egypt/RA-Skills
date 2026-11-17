# Optional Agent stage observer

An Agent host that can observe these stages may import `scripts/h08-stage-observer.mjs` and call
`createH08StageObserver({ locale, skillParent, report, canReport, privacySignals })` once per task.
`skillParent` is the absolute local directory containing the Creator and Publish Skill folders.
`report(payload)` is the host's existing authenticated `onimi_report_agent_event` call; the observer
does not obtain OAuth credentials or make network requests. `canReport` must reflect whether that tool
is currently available with a bearer, and `privacySignals` must return the host's current boolean
`dnt` and `gpc` values. An unknown signal suppresses reporting. Keep the observer in memory only; its
random analytics task ID is separate from `task-state.mjs` and is discarded with the task. This local
check does not prove which DNT/GPC headers the host sends; the host must preserve the actual request
signals, and the server applies its own header and consent policy on every delivery.

Call `startTask(kind)` after user confirmation, then `capabilityReady(module)` after the local check.
Call `authorizationOpened(reason)` only when this client opened the actual browser consent window;
without a bearer that stage is omitted immediately. Pass the actual `onimi_get_connection` response,
expected current actor, required scopes and `state: "reused"|"after_authorization"` to
`connectionResult`. For first preview, call `firstVisiblePreview({visible:true,firstForTask:true,
artifactKind})` only after the host has a visible-render receipt for this task; hidden, loading, or
old previews are not receipts. The observer uses a monotonic clock and subtracts observed browser
authorization waiting from Agent time. For other real user pauses, pair `userWaitStarted()` and
`userWaitEnded()` at the actual pause boundaries; an unclosed wait suppresses first-preview reporting.
If either clock or visibility is unknown, omit the event.

For publication, call `beginPublication({businessMutationId,kind,projectId,publicationId?})` once
for the exact prepare/activate request. `businessMutationId` is the request's stable idempotency UUID;
the returned analytics `operationId` is a separate short-term random UUID and remains stable for this
operation. Call `publicationAttempt(operationId,businessMutationId)` immediately before each **actual**
send, including a retry of the unchanged request. Pass the actual parsed MCP result to
`publicationResponse({operationId,response})`; the observer reads its `projectId`, `publicationId`,
`status`, `idempotencyKey`, and `idempotentReplay`, then constructs only the reviewed event fields. These values
must come from that response, never from the request or journal. It reports a `pending-review` prepare as
`pending` and an active activation as `active`. It leaves timeouts, unreadable replies, status reads,
and unverified errors empty. A telemetry delivery whose receipt is uncertain may use
`retryDelivery(reportId)` with the unchanged report ID and payload; this never retries the business
operation. Reporter errors never block the business flow. This local helper and its tests do not
establish a hosted capture receipt or client acceptance.
