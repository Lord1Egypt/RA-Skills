# OpenClaw Triage Checklist

Use this quick sort before diving deep.

## 1. Ingress
Question: did OpenClaw receive the event at all?

Check:
- channel membership / installation
- privacy / permissions where applicable
- whether a fresh inbound event created or updated the expected session

## 2. Routing
Question: did the event land in the correct session/chat/thread/group?

Check:
- exact chat or channel ID
- topic/thread bindings
- migrated IDs or stale bindings
- whether delivery context matches the real surface

## 3. Authorization
Question: was the sender allowed to trigger the behavior?

Check:
- `allowFrom`
- `groupAllowFrom`
- policy mode (`allowlist`, `pairing`, `open`)
- command-specific authorization behavior

## 4. Runtime / provider
Question: did the model/tool/runtime execute successfully?

Check:
- provider auth
- rate limits / timeouts
- fallback behavior
- subagent availability

## 5. Delivery
Question: did the reply land where the user expected?

Check:
- target chat ID
- topic/thread context
- reply mode
- message acceptance vs visible placement

## Principle
Never collapse these layers into one vague diagnosis. Name which layer failed.
