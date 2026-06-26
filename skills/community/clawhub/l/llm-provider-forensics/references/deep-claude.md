# Claude Native Deep Tests

Use when native Anthropic-compatible route works.

## Deep probes
- long context recall under `/v1/messages`
- strict JSON-only output
- refusal style on edge-case unsafe prompt
- repeated variance on same free-form prompt
- malformed body error schema check

## Native clues
- clean `content` array with text blocks
- anthropic-style error body or request validation
- stable behavior under `anthropic-version` header
