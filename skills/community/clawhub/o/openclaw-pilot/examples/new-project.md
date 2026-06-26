# Example: new project

## Input

```text
/pilot I want to turn rough product ideas into executable OpenClaw instructions, but start with the smallest publishable behavior and do not overbuild the host integration layer.
```

## Expected shape

### Message 1

A human-readable blueprint that covers:

- current project goal
- current stage
- why this stage now
- in-scope and out-of-scope
- what should be sent back to `/pilot`
- the next continuation command

### Message 2

A separate pure packet message:

```text
[OPENCLAW_EXECUTION_PACKET v1]
...
[END_OPENCLAW_EXECUTION_PACKET]
```

## Why this matters

This lets the user inspect the plan first, then hand the packet directly to OpenClaw without manually extracting it from mixed prose.