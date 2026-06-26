# Prompt Migration

Use this reference when migrating hardcoded prompts or message arrays into Langfuse prompt management.

## What to preserve

Preserve these first:

- prompt intent
- variable semantics
- system/user role structure
- runtime defaults
- labels/environment selection

Do not start by rewriting prompt content stylistically unless the user asks. First make the prompt managed, versioned, and fetchable.

## Recommended migration workflow

1. Find prompt literals in the codebase.
2. Group them by purpose and runtime call site.
3. Name each Langfuse prompt clearly.
4. Convert inline variables into Langfuse placeholders such as `{{variable}}`.
5. Create the prompt in Langfuse as either:
   - `text`
   - `chat`
6. Replace inline literals with runtime fetches.
7. Render/fill variables at the call site.
8. Verify output parity.
9. If feasible, link prompt usage to traces so metrics and evals can be segmented by prompt version.

## Prompt naming guidance

Prefer names that describe behavior, not implementation details.

Good examples:

- `support-answer-drafter`
- `sql-debug-assistant`
- `agent-router-system`
- `lead-enrichment-summary`

Avoid names like:

- `prompt1`
- `new-chat-prompt`
- `prod-copy-final-v2`

## Data model reminders

- Prompts can be `text` or `chat`.
- Creating a prompt with the same `name` adds a new version.
- Labels can be used to promote versions, such as `production`.
- Runtime fetching should use client helpers instead of raw API calls when possible.

## Python examples

### Create a text prompt

```python
langfuse.create_prompt(
    name="movie-critic",
    type="text",
    prompt="As a {{criticlevel}} movie critic, do you like {{movie}}?",
    labels=["production"],
)
```

### Create a chat prompt

```python
langfuse.create_prompt(
    name="movie-critic-chat",
    type="chat",
    prompt=[
        {"role": "system", "content": "You are an {{criticlevel}} movie critic"},
        {"role": "user", "content": "Do you like {{movie}}?"},
    ],
    labels=["production"],
)
```

### Runtime fetch guidance

At runtime, prefer the dedicated prompt fetch helper mentioned in Langfuse docs:

- Python: `get_prompt`
- JS/TS: `getPrompt`

Use these instead of reaching into generic API endpoints for normal application prompt retrieval.

## JS/TS examples

### Create a text prompt

```ts
await langfuse.prompt.create({
  name: "movie-critic",
  type: "text",
  prompt: "As a {{criticlevel}} critic, do you like {{movie}}?",
  labels: ["production"],
});
```

### Create a chat prompt

```ts
await langfuse.prompt.create({
  name: "movie-critic-chat",
  type: "chat",
  prompt: [
    { role: "system", content: "You are an {{criticlevel}} movie critic" },
    { role: "user", content: "Do you like {{movie}}?" },
  ],
  labels: ["production"],
});
```

## API example

```bash
curl -X POST "https://cloud.langfuse.com/api/public/v2/prompts" \
  -u "your-public-key:your-secret-key" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "chat",
    "name": "movie-critic",
    "prompt": [
      { "role": "system", "content": "You are an {{criticlevel}} movie critic" },
      { "role": "user", "content": "Do you like {{movie}}?" }
    ]
  }'
```

## Migration review checklist

- Prompt names are stable and readable.
- Variables use Langfuse placeholder syntax.
- Prompt type matches runtime usage.
- Labels reflect deployment intent.
- Code no longer depends on duplicated inline prompt blobs.
- Prompt fetch path is centralized where practical.
- Prompt-version metrics can be tied back to runtime traces when useful.
