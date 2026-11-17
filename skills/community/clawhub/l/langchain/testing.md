# Testing — Deterministic Tests For Nondeterministic Systems

Split the system in two: the plumbing (prompt variables, routing, tool schemas, parsing, state) is ordinary software and must be tested deterministically; the quality of what the model says is an evaluation problem with a different cadence.

## Fake Models

```python
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage

model = GenericFakeChatModel(messages=iter([AIMessage("canned answer")]))
assert chain.invoke({"question": "x"}) == "canned answer"
```

- `GenericFakeChatModel` returns queued messages and supports streaming, so it exercises the streaming path too. `FakeListLLM` / `FakeListChatModel` are the simpler list-based variants.
- Queue several messages to test an agent loop: first a message with `tool_calls`, then the final answer. That covers the tool-execution path with zero API calls.
- Fake models do not validate your schema. Pair them with a schema assertion (`tool.args_schema.model_json_schema()`) so a renamed field still fails a test.

## What To Assert Deterministically

| Target | Assertion |
|---|---|
| Prompt wiring | `prompt.invoke(inputs).to_string()` contains the context and the question, and no `{` survived |
| Chain contract | `chain.input_schema.model_json_schema()` — a breaking refactor fails here, not in production |
| Tool schemas | Names match the provider pattern, every field has a description, injected args are absent from the schema |
| Tool logic | Call the tool directly with edge-case arguments; assert the error text is actionable |
| Routing | With a fake model returning each route token, the right branch runs |
| Parsers | Feed recorded raw outputs (including the malformed ones) and assert the failure path |
| State reducers | Apply two concurrent updates and assert the merge, no model involved |
| Trimming | A history with a tool-call pair at the boundary keeps or drops the pair together (SKILL.md Core Rule 7) |

Never assert exact model prose. `temperature=0` is not determinism, and a test that pins wording breaks on the next model revision for no reason.

## Recorded Fixtures

- Capture real provider responses once and replay them (VCR-style HTTP recording, or a fake model seeded from saved messages). Malformed outputs collected from production are the highest-value fixtures you will ever have.
- Scrub keys and PII at record time — fixtures live in the repo forever.
- Re-record deliberately on a model upgrade; a passing suite against year-old fixtures proves only that your code still parses last year's model.

## Cheap Live Tests

When a test must hit the provider:

- Enable response caching so a rerun of the suite is nearly free and repeatable within the cache lifetime.
- Mark them separately (`pytest -m live`) and keep them out of the fast pre-commit run.
- Cap the blast radius: smallest model, tiny `max_tokens`, and a hard timeout so a stalled provider cannot hang CI.
- Assert properties, not text: the object validates, the fields are non-empty, the number is in range, the citation exists in the retrieved context.

## Evaluating Quality

- Build the dataset from real inputs (production traces, support tickets), not invented ones. A small set of real cases beats a much larger synthetic one: invented inputs inherit the author's assumptions, so they pass for the same reason the code does.
- Score with cheap deterministic checks first: does the answer contain the required id, is the JSON valid, did retrieval return the known-good document at any rank. Reserve LLM-as-judge for the genuinely subjective remainder (`llm-as-judge` skill).
- Retrieval and generation are scored separately — a bad answer over a bad context is a retrieval bug and no amount of prompt work fixes it (`rag-evaluation` skill).
- Run the eval on every prompt or model change, and store the score with the commit. Prompt edits are code changes with no compiler; the eval is the only regression signal you have.

## CI Shape

1. Fast lane, no network: fake models, fixtures, schema and routing assertions. Runs on every commit.
2. Nightly or pre-release: live smoke tests plus the eval set, with a threshold that fails the build on regression.
3. Dependency guard: pin the langchain packages and run the fast lane against a scheduled upgrade PR — that is where a moved import gets caught before a deploy does it for you.
