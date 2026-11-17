# Scheduling agent workflows

## Reuse a mailbox

1. Call `list_mailboxes`. Prefer a mailbox with `can_receive` true and receiving status ready.
2. Reject disabled, non-receiving, cross-workspace, ambiguous, or verification-isolated mailboxes.
3. Create only when the user authorizes a new inbox and no suitable one exists. Do not set `agentInbox.mode` to `verification`.

## Connect Google Calendar

1. Call `list_composio_toolkits` / `list_composio_connections` for slug `googlecalendar`.
2. If already `ACTIVE`, skip connect.
3. Otherwise call `connect_composio_toolkit` once, present the exact `redirectUrl`, and pause.
4. After the user confirms browser completion, call `sync_composio_connections` once, then re-list connections.
5. Continue only when status is `ACTIVE`. Do not claim connected from a redirect alone.

## Offer real slots

1. Parse requested windows, timezone, duration, and attendees from the selected clean message. Ask when any of those are missing.
2. Call `get_composio_calendar_account` when the connected calendar email is needed.
3. Search for the smallest free/busy or list-events action, inspect its schema, then execute once with a bounded time range.
4. Offer 1–3 slots that the read shows as free. Never invent availability.

## Confirm a chosen slot

1. Preview event title, start/end, timezone, attendees, and calendar account. Obtain approval.
2. Execute the event-create action once. Require `successful: true` before claiming the hold.
3. Preview the Mermail confirmation recipients and body. Obtain send approval separately.
4. Reply or send once with one idempotency key. Verify the authoritative sent/scheduled result.
5. If the calendar write is uncertain, inspect provider state once and do not send a confirmation that claims the event exists.
