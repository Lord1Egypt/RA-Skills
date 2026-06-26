# Promptfoo example notes

These notes distill patterns observed in Promptfoo's own docs and example directories.

## Common structural choices

Promptfoo examples commonly include:

- `# yaml-language-server: $schema=https://promptfoo.dev/config-schema.json`
- a short top-level `description`
- `prompts`, `providers`, and `tests`
- `vars` under each test case
- `defaultTest.assert` when assertions are shared
- `file://...` references for prompts and local assets

## Example families

### getting-started

Pattern:

- simple inline prompt strings
- multiple providers
- lightweight deterministic assertions
- intended to demonstrate the prompt x provider x test matrix

Use as a baseline for first-time Promptfoo work.

### eval-self-grading

Pattern:

- prompt loaded from `file://prompts.txt`
- shared grading logic in `defaultTest`
- mix of rubric and javascript scoring

Use when many tests share the same expectations and prompt text is easier to maintain in a file.

### compare-openai-models

Pattern:

- same prompt and tests across multiple providers
- `defaultTest` cost and latency thresholds
- test-level assertions for correctness

Use when the question is which provider or model wins on a specific workload.

### eval-rag

Pattern:

- inline multi-line prompt with `{{query}}` and `{{context}}`
- local docs referenced with `file://...`
- RAG-specific metrics like `factuality`, `answer-relevance`, `context-recall`, `context-relevance`, `context-faithfulness`

Use when quality depends on grounding, not just answer wording.

### openai-agents-basic

Pattern:

- prompt is often just `{{query}}`
- richer provider object with `id` and `config`
- file-backed agent and tool definitions
- assertions mix rubric and custom javascript logic

Use when evaluating a real agent loop or tool-using workflow.

## Practical implications for skill users

When adapting Promptfoo to a repo:

- prefer matching one of Promptfoo's existing example families
- use file-backed prompts or assets when the repo already organizes content that way
- use `defaultTest` to reduce repetitive assertions
- use targeted metrics instead of overloading `llm-rubric`
- evaluate the real target path when app behavior matters more than prompt text alone
