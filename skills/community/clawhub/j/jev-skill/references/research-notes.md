# Jev Skill research notes

Research date: 2026-09-22.

These notes distill the current official TypeSafe documentation into routing
guidance. The live pages remain authoritative.

## Video-derived control-plane notes

Transcript source: [LangChain — Building a Harness with Jev](https://youtu.be/VE5dsWll06M)
(9:14, captions retrieved 2026-09-22). The speaker presents Jev as a fast,
typed decision layer around a slower open-ended agent and demonstrates three
control-plane uses: model routing by task complexity, pre-tool risk gating,
and online rubric judging of agent answers for correctness, grounding, and
citation.

The video’s speed, cost, and reliability comparisons are claims from the
presentation, not benchmarks produced by this repository. We used the
architecture pattern, not those claims, to add
[`scripts/jev_control.py`](../scripts/jev_control.py):

- route only when the Choice distribution clears both a confidence and a
  runner-up-margin threshold;
- fail closed for malformed or unavailable risk judgments, while keeping
  authorization deterministic and outside the model;
- aggregate explicit typed rubric criteria into `accept`, `review`, or
  `reject` so online evaluation can abstain instead of forcing a grade.

## Official source map

- Documentation index: <https://docs.typesafe.ai/llms.txt>
- Quick start: <https://docs.typesafe.ai/introduction/quickstart.md>
- System One: <https://docs.typesafe.ai/concepts/system-one.md>
- State: <https://docs.typesafe.ai/concepts/state.md>
- Questions: <https://docs.typesafe.ai/primitives.md>
- Choice: <https://docs.typesafe.ai/primitives/choice.md>
- Score: <https://docs.typesafe.ai/primitives/score.md>
- Noul: <https://docs.typesafe.ai/primitives/noul.md>
- Confidence: <https://docs.typesafe.ai/confidence.md>
- How to build: <https://docs.typesafe.ai/concepts/how-to-build-with-system-one.md>
- Intent routing: <https://docs.typesafe.ai/patterns/intent-routing.md>
- Confidence routing: <https://docs.typesafe.ai/patterns/confidence-routing.md>
- Fan-out: <https://docs.typesafe.ai/patterns/fan-out.md>
- Composite scoring: <https://docs.typesafe.ai/patterns/composite-scoring.md>
- HTTP API: <https://docs.typesafe.ai/api.md>
- Models and limits: <https://docs.typesafe.ai/models.md>
- Jev 1.13 jaggedness: <https://docs.typesafe.ai/model-jaggedness/jev-1.13.md>
- Python SDK: <https://docs.typesafe.ai/sdk/python.md>
- JavaScript SDK: <https://docs.typesafe.ai/sdk/javascript.md>
- Python retry policy: <https://docs.typesafe.ai/sdk/python/retries.md>
- Python responses and request IDs: <https://docs.typesafe.ai/sdk/python/responses.md>
- Official TypeSafe agent skill: <https://github.com/typesafe-ai/skills/tree/main/skills/typesafe-ai>
- Official Python SDK: <https://github.com/typesafe-ai/typesafe-sdk-python>
- Official JavaScript SDK: <https://github.com/typesafe-ai/typesafe-sdk-js>
- Official System One adapter: <https://github.com/typesafe-ai/system-one-adapter-python>
- Community OpenJev local scorer: <https://github.com/daseinlabs/open-jev>
- OpenJev open-weight NLI model card and SGLang server: <https://huggingface.co/AlexWortega/openjev>
- Community LocalJev Bun bridge: <https://github.com/githubnext/localjev>
- Von open System One decision server: <https://github.com/wfzyx/von>
- Laya open non-autoregressive decision engine: <https://github.com/NandhaKishorM/laya>
- LitJev Qwen decision-layer reproduction: <https://github.com/zhengxuyu/litjev>
- Simple-JEV next-token-logit server: <https://github.com/featherless-ai/simple-jev>
- poorjev calibration-first local decision layer: <https://github.com/rupeshpoojary9/poorjev>
- NanoJev parallel game decision model: <https://github.com/TianyuCodings/NanoJev>
- JevBench benchmark repository: <https://github.com/fstandhartinger/jevbench>
- OpenLayer jevals agent evaluation/guardrails: <https://github.com/openlayer-ai/jevals>
- LangChain Jev harness article: <https://www.langchain.com/blog/building-a-harness-with-jev>
- LangChain Jev harness video: <https://youtu.be/VE5dsWll06M>
- LangChain TypeSafe integration package: <https://pypi.org/project/langchain-typesafe/>
- Jev-class model comparison and JevBench protocol: <https://benchmarkheaven.com/jev-models>
- vLLM structured outputs: <https://docs.vllm.ai/en/latest/features/structured_outputs/>
- Ollama structured outputs: <https://github.com/ollama/ollama/blob/main/docs/capabilities/structured-outputs.mdx>
- LM Studio structured output: <https://beta.lmstudio.ai/docs/developer/openai-compat/structured-output>
- llama.cpp server and OpenAI-compatible API: <https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md>
- llama.cpp grammars and LLGuidance: <https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md>
- Inspect AI evaluation framework: <https://github.com/UKGovernmentBEIS/inspect_ai>
- EleutherAI lm-evaluation-harness: <https://github.com/EleutherAI/lm-evaluation-harness>
- OpenAI Evals: <https://github.com/openai/evals>
- Stanford HELM: <https://github.com/stanford-crfm/helm>
- Self-consistency: <https://arxiv.org/abs/2203.11171>
- Step-level verification: <https://arxiv.org/abs/2305.20050>
- Self-verification: <https://arxiv.org/abs/2212.09561>
- Calibration survey and metrics: <https://arxiv.org/pdf/2207.13770>
- Qwen3 concepts and thinking modes: <https://github.com/QwenLM/Qwen3/blob/main/docs/source/getting_started/concepts.md>
- DeepSeek-R1 model card: <https://huggingface.co/deepseek-ai/DeepSeek-R1>
- DeepSeek-R1 release: <https://deepseek.com/en/news/deepseek-r1/>

## Findings that affect implementation

### Programming model

Jev is the flagship TypeSafe System One model. The request evaluates one state
against one or more typed questions and returns structured answers. The model
supplies semantic judgment; application code owns workflow, policy, arithmetic,
thresholds, and side effects.

### State

State can be a string, JSON object, or array of text values. A named object is
usually the clearest form for tickets, conversations, records, and policies.
The documented interface does not accept images, audio, or video as state.
Questions are independent when sent together and all see the same state.

### Primitives

| Type | Use it for | Returned signal |
| --- | --- | --- |
| Noul | A yes/no condition; several labels may apply | probability that yes is true |
| Choice | Exactly one option from a defined set | selected choice, probabilities, confidence |
| Score | An ordered degree or severity scale | score, legend, probabilities, confidence |

The question ID is a local key for the returned answer. The model sees the
instructions and criteria, not the ID. A Choice needs complete candidate
coverage, and Score criteria must describe concrete ordered levels.

### Uncertainty

Choice and Score confidence is derived from their probability distribution. It
describes concentration, not truth, permission, or overall workflow accuracy.
A Noul's yes probability is its uncertainty signal and has no separate
confidence field. Thresholds should be tuned against representative outcomes
and the cost of each mistake.

### API and SDK

The current quick start documents:

```text
POST https://api.typesafe.ai/v1/systemone
Authorization: Bearer <API_KEY>
```

The API request uses `state`, `model`, and `questions`. The documented current
alias is `jev-latest`. The Python SDK package is `typesafe-sdk`, requires Python
3.10 or newer, and reads `TYPESAFE_API_KEY` from the environment by default.
Use the current SDK/API pages for exact version-specific constructors and error
types.

The official models page currently lists Jev 1.13.0 as `jev-1.13.0`. The
`jev-latest` alias currently points to it, but aliases can move; the response
reports the resolved version. Pin a version for a benchmark whose thresholds
must be reproducible, and run a canary before moving the pin. The page also
lists a 64k request context, with up to 32k tokens reserved for state plus the
longest question, text-only input, and dynamic rate limits. Treat those values
as operational configuration, not permanent constants. The listed input price
is $42 per billion tokens ($0.042 per million) with output tokens free at the
time of this research; the harness therefore requires pricing flags instead of
silently baking a price into reports.

The official JavaScript SDK currently targets Node.js 20+, while the Python SDK
supports Python 3.10+. Both SDKs expose typed responses. The Python response
surface exposes a request ID from `x-typesafe-request-id` and usage may be
optional, so the harness records request IDs when available and treats absent
usage as a warning rather than misclassifying an otherwise valid answer. The
documented Python retry policy retries connection/timeouts and transient HTTP
failures with bounded exponential backoff, jitter, and `Retry-After` support;
the included dependency-free runner mirrors those safeguards for raw HTTP.

### Architecture patterns

The official docs emphasize intent routing, confidence-gated routing,
speculative fan-out, composite scoring, verification, extraction, and
cascades. The best first design is usually: retrieve or assemble state → ask
small independent judgments → combine or threshold in code → route to a
deterministic handler, specialist model, or human.

### Reliability

The API documents `401` for authentication failures and `429`/`529` for rate
limits or overload. Retry transient failures with exponential backoff; the
official SDKs provide a default retry policy. Keep credentials server-side and
avoid logging sensitive state by default.

### Failure modes worth testing

The official Jev jaggedness notes describe uneven performance rather than one
single global weakness. Build tagged cases for literal interpretation,
arithmetic and numeric representations, dates and times, indirection,
contradictory instructions or criteria, adversarial content, structural
invariants, generation errors, and oversized or irrelevant state. The latter
is especially important: irrelevant context can degrade a judgment even when
the relevant fact is present (context rot). Record state size and split metrics
by tags so a clean aggregate cannot hide a dangerous slice.

Use a three-layer evaluation set:

1. Stable golden cases with human-reviewed expected answers.
2. Metamorphic cases where irrelevant or reordered evidence should not change
   the answer.
3. Boundary/adversarial cases that should trigger a safe route or human review.

Do not treat model confidence as a correctness guarantee. For Choice and
Score, calibrate confidence against labeled outcomes and report selective
coverage/accuracy at the production threshold. For Noul, use the raw yes
probability with Brier and log loss, then choose thresholds from the cost of
false positives and false negatives.

## Useful cookbooks

Read only when the task matches:

- Function calling: <https://docs.typesafe.ai/cookbooks/function_calling.md>
- Parallel questions: <https://docs.typesafe.ai/cookbooks/parallel_questions.md>
- Guardrails: <https://docs.typesafe.ai/cookbooks/llm_guardrails.md>
- Citation checks: <https://docs.typesafe.ai/cookbooks/citation_check.md>
- Pre-parsed value extraction: <https://docs.typesafe.ai/cookbooks/pre_parsed_value_extraction_cookbook.md>
- SDE cascade: <https://docs.typesafe.ai/cookbooks/sde_cascade.md>
- Classification using confidence: <https://docs.typesafe.ai/cookbooks/classification_using_confidence.md>

## Harness design decisions

The included harness is intentionally dependency-free so it can run in CI
without importing an SDK. It validates the full typed response contract before
scoring; records the resolved model, request ID, retry attempts, state byte
size, latency percentiles, token totals, and optional cost; and never writes
the API key or raw state into its report. It also produces per-question and
per-tag slices, confusion matrices, Brier/log loss, Score MAE/RMSE, expected
calibration error, and selective confidence metrics. Use `--model
jev-1.13.0` for a pinned benchmark and `jev-latest` for a moving canary.

### Local-model path

The local path is deliberately a contract-and-reliability layer, not a claim
of weight-level parity with Jev. The harness sends the same state plus typed
Noul/Choice/Score definitions to a local runtime, requests JSON-schema
constrained output where the runtime supports it, validates the response in
Python, and keeps policy and thresholds outside the model. vLLM, LM Studio,
and llama.cpp expose OpenAI-compatible structured-output routes; Ollama
exposes a native `format` JSON-schema field. The provider adapters are small
so a local runtime can be swapped without changing question definitions or
evaluation records.

### Open Jev-compatible runtimes

The community `daseinlabs/open-jev` project is a useful local interoperability
target: it implements a `/v1/systemone` route over a one-pass option scorer and
also exposes a lower-level `/score` route. Its documented implementation uses
MLX and a local Gemma checkpoint on Apple Silicon. The Jev Skill harness calls
the typed route directly through `--provider openjev`, preserving the same
question files and report schema used for hosted Jev and other local runtimes.

The `AlexWortega/openjev` Hugging Face repository is a separate open-weight
implementation, not an alternate URL for the daseinlabs server. Its model card
describes Qwen3.5 cross-encoder checkpoints trained as three-way NLI models,
with labels ordered contradiction, entailment, and neutral. The published
`modeling_openjev.py` exposes direct Transformers inference and optimized
shared-prefix hypothesis scoring; its `code/` directory also supplies an
SGLang external model package and client. The SGLang client posts text batches
to `/classify` and reads raw logits from each `embedding` field. The model card
lists a 0.8B long-context variant, a recommended 4B v2 text+image variant, and
a 35B-A3B MoE variant, plus an MIT license.

Jev Skill's `openjev-hf` adapter targets that SGLang route without copying the
model files. It sends the state as the NLI premise and turns each Choice/Score
criterion into a hypothesis using the card's `The correct answer is: ...`
pattern. It converts NLI logits with softmax, normalizes entailment scores over
options, and maps a Noul to entailment plus half of neutral mass. This makes
the checkpoint measurable under the shared harness contract, but those derived
probabilities are not direct Jev probabilities and require independent
calibration. The current adapter serializes text/JSON state; image-capable
inference remains a future extension.

This is compatibility, not weight parity. Benchmark Heaven's JevBench page
lists several independent Jev-class rebuilds, including OpenJev, SemIf, and
open-alternative-jev, while identifying TypeSafe's Jev as closed. Treat each
rebuild as a separate model with its own calibration, license, model-card, and
distribution checks. Do not copy upstream source or redistribute checkpoints
without confirming the upstream repository and model licenses.

`githubnext/localjev` is a complementary MIT-licensed TypeScript/Bun bridge.
It exposes the same `/v1/systemone` contract on port `8080`, translates typed
questions into a classification prompt, asks an OpenAI-compatible
DiffusionGemma endpoint for scalar/vector probabilities, normalizes them, and
calculates Jev-compatible answers. It adds useful operational patterns—an
in-flight semaphore, bounded queue with `529` overload responses, malformed
JSON retries, question/outcome chunking, and repeatable model bake-offs.

The bridge is portable, but its probabilities are generated/self-reported by
the model and therefore are not mathematically equivalent to OpenJev's direct
logit read. The harness exposes it as `--provider localjev` so its calibration,
latency, retries, and review rate remain visible as a separate model path.

### Additional open implementations

The ecosystem now has several native or near-native implementations. The
harness registers the providers whose repositories document the TypeSafe-shaped
`POST /v1/systemone` route:

- **Von** (`wfzyx/von`) documents an Apache-2.0 local server, a native route,
  direct typed answers, and post-training temperature scaling. Its accuracy,
  speed, and calibration numbers are upstream claims until reproduced under
  this repository's matched cases.
- **LitJev** (`zhengxuyu/litjev`) runs Qwen checkpoints and reads label scores
  directly from the output head. Its documentation explicitly says the raw
  probabilities are not calibrated by default; treat it as a separate direct
  logit model, not TypeSafe weights.
- **Simple-JEV** (`featherless-ai/simple-jev`) reads selected next-token logits
  and exposes `/v1/systemone` as an alias of `/v1/classifier`. It is Apache-2.0
  code, but token-boundary, prompt-template, branch-count, and context limits
  remain model/server constraints.

**Laya** (`NandhaKishorM/laya`) is an in-process Python decision engine with
Apache-2.0 code and checkpoint-specific language/cardinality constraints. The
Simple-JEV server can load a Laya backend, which is the cleanest way to bring
it under this harness without inventing a new in-process dependency path.
Laya's own benchmark notes that high-cardinality choices and raw calibration
need special treatment.

**poorjev** (`rupeshpoojary9/poorjev`) is a separate MIT-licensed local layer
whose strongest contribution is reproducible calibration and abstention
measurement. It exposes Python/MCP primitives rather than the harness's native
HTTP route, so Jev Skill does not claim a first-class adapter for it yet.

**NanoJev** (`TianyuCodings/NanoJev`) is a MIT-licensed, task-specific parallel
decision project with its own `/api/evaluate` service and game-heavy releases.
Its architecture is worth studying for batch/action distributions, but its
results should not be pooled with general typed-decision accuracy without a
matched adapter and task split.

The implementation details and fair-comparison rules are consolidated in
[ecosystem.md](ecosystem.md). The new `fit_calibration.py` utility deliberately
fits only on labeled harness reports and stores no raw state; the new
`compare_reports.py` utility refuses mismatched question/case hashes by
default.

### LangChain agent integration

LangChain's Jev integration is a separate hosted control-plane surface. The
official package exposes `TypeSafeClassifier` as a LangChain Runnable and
supports `Noul`, `Choice`, and `Score` question objects. Its experimental
middleware currently includes:

- `ModelRouterMiddleware`: classify the latest human message in `before_agent`,
  store the complete `ChoiceAnswer`, and use the selected model for every model
  call in that run.
- `AutoModeMiddleware`: classify configured tool calls immediately before
  execution, block calls at or above its risk threshold, and fail closed when
  classification fails. Tools not listed in the middleware configuration pass
  through.

This makes Jev a control-plane classifier, not the agent's generative model.
The middleware does not establish authorization, ask a human for approval, or
enforce path, credential, spend, or side-effect policy. Keep those controls in
deterministic runtime code. Treat tool arguments, web content, files, and
model output as attacker-reachable state and evaluate prompt-injection cases.

The package's experimental extra currently requires the LangChain agent
framework and is version-sensitive. Keep it optional in Jev Skill: hosted
LangChain calls use `langchain-typesafe`, while local `openjev`, `openjev-hf`,
and `localjev` remain measured through this repository's provider harness.
Do not compare a middleware's tool-block rate with model accuracy without
recording the agent outcome, false blocks, bypassing tools, and policy
overrides.

Structured decoding is a syntax guarantee, not a semantic truth guarantee.
The strongest practical stack implemented here is:

1. strict schema validation and no JSON-repair by default;
2. independent test-time samples with distribution averaging and agreement;
3. a separate typed verifier over the evidence and candidate answer;
4. explicit abstention to human/rule review when consensus or verifier
   support is low;
5. golden, metamorphic, boundary, adversarial, and context-rot slices;
6. calibration and CI gates measured on the deployment model, not assumed from
   generic confidence values.

Self-consistency and process/self-verification research motivates the ensemble
and verifier layers, but neither is a correctness proof. A verifier can share
the same blind spot as the answer model; use a different model or a
deterministic checker for high-risk claims when possible. Arithmetic, dates,
permissions, and other exact invariants should remain code-owned.

Local model families change quickly. Qwen's official documentation describes
hybrid thinking/non-thinking operation; DeepSeek's official R1 release makes
local reasoning weights available; and provider catalogs change model names
and support over time. Treat the model name, runtime flags, context limits,
grammar support, and quantization as benchmark inputs. Do not hard-code a
claim that any local checkpoint matches Jev until the same golden suite,
failure slices, latency, cost, and calibration results demonstrate it.
