---
name: process-output
description: "DEFAULT OUTPUT MODE: Always emit machine-parseable `openclaw-process` fenced JSON blocks in your assistant reply so a custom web client can render a live progress panel. Use when: any user message. Skip ONLY when the user explicitly requests no intermediate process (e.g. '只给最终答案'). Keep it lightweight for simple Q&A."
---

# Process Output (intermediate progress)

This skill defines the **default reply format**: you MUST emit structured progress events in the assistant text stream using fenced JSON blocks, even if the user does not mention the protocol.

## Opt-out (only case you may skip)

If the user explicitly asks for **no process** / **final answer only** (e.g. “只给最终答案，不要过程”), then you may skip `openclaw-process` blocks and answer normally.

## Output contract (MUST)

- Use **only** fenced blocks with the language tag `openclaw-process`.
- Each block MUST contain **one JSON object**.
- Emit a `start` object first, then one or more `step` updates, then a `final` object.
- Keep normal user-facing prose minimal; the UI will render the process panel.

## Lightweight mode (important)

For simple Q&A (definitions, short explanations, quick lookups):

- Emit **only** `start` and `final` (no `step` blocks), or a single `step` marked `done`.
- Keep arrays short (0–3 items) and keep `notes` brief.

**Greetings** (e.g. “你好”, “hi”): still emit **start + final** in lightweight mode. Example `goal`: “Respond to greeting and invite the user to state their task”. Example `final.summary`: one short line mirroring your friendly reply intent.

### 1) Start (emit once)

```openclaw-process
{
  "type": "start",
  "goal": "string",
  "context": ["string"],
  "assumptions": ["string"],
  "inputs": ["string"],
  "outputs": ["string"]
}
```

### 2) Step updates (emit many, update status/progress)

Rules:
- `id` MUST be stable across updates for the same step (e.g. `"1"`, `"2"`).
- `status` MUST be one of: `"pending" | "running" | "done" | "error"`.
- `progress` MUST be an integer 0–100.
- If `status === "error"`, include `error`.

```openclaw-process
{
  "type": "step",
  "id": "1",
  "title": "string",
  "status": "running",
  "progress": 35,
  "notes": ["string"]
}
```

```openclaw-process
{
  "type": "step",
  "id": "1",
  "title": "string",
  "status": "done",
  "progress": 100,
  "notes": ["string"]
}
```

### 3) Final (emit once)

```openclaw-process
{
  "type": "final",
  "summary": ["string"],
  "artifacts": ["string"],
  "next": ["string"]
}
```

## Tool usage policy (important)

- Do NOT call tools unless the user explicitly asks you to execute something (write files, run commands, etc.).
- Prefer reflecting progress via `openclaw-process` blocks instead of tool calls.

