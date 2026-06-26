# Example: continuation

## Input

```text
/pilot next pilot-abc123 STATUS: blocked SUMMARY: the release docs are mostly done, but the packet message still includes human explanation in one branch.
```

## Expected behavior

- reuse the same pilot lineage
- advance the current stage using the supplied feedback
- return two messages again
- keep the second message as a pure execution packet only

## Continuation contract

The continuation path must follow the same delivery contract as a new `/pilot` request:

1. human-readable blueprint message
2. separate packet-only message

If continuation drifts back to a single combined reply, that is a contract regression.