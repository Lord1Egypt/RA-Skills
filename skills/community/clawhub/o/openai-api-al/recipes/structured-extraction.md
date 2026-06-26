# Recipe — Structured Extraction

## Goal

Extract structured JSON from unstructured text reliably.

## When

Parsing entities, fields, or records from free text (invoices, emails, notes) for downstream code.

## Inputs

- The source text.
- A target JSON schema.
- A cheap model (`gpt-4o-mini`).

## Steps

1. Moderate untrusted input if applicable.
2. Define the JSON schema you want.
3. Call `openai_chat` with `response_format` (`json_object` or `json_schema`) — or `openai_responses` with `text.format`.
4. Set `max_tokens` and low `temperature` (0–0.2) for stable output.
5. **Parse and validate** the returned JSON against your schema.
6. Report `usage`.

## Output

A validated JSON object.

## Example

```json
{
  "tool": "openai_chat",
  "arguments": {
    "model": "gpt-4o-mini",
    "messages": [
      { "role": "system", "content": "Extract fields as JSON: {name, email, amount}." },
      { "role": "user", "content": "Invoice from Jane Doe (jane@x.com) for $250." }
    ],
    "response_format": { "type": "json_object" },
    "temperature": 0,
    "max_tokens": 80
  }
}
```

Result content:

```json
{ "name": "Jane Doe", "email": "jane@x.com", "amount": 250 }
```

## Edge cases

- Invalid JSON returned → retry once with stricter instructions, or use `json_schema` to enforce shape.
- Missing fields → allow `null` in the schema and handle downstream.
- Ambiguous text → keep `temperature` at 0 and add few-shot examples.

## Production notes

- **Cost:** `gpt-4o-mini` with a tight `max_tokens` is ideal. Don't escalate unless extraction quality fails.
- Prefer `json_schema` for guaranteed structure over post-hoc regex.
- Always validate before trusting the JSON in code.

> Verification needed: confirm `response_format`/`json_schema` support with <https://platform.openai.com/docs/api-reference>.
