# Jev Skill — Open-Source Typed AI Decision Harness

Jev Skill is an open-source typed AI decision harness for Jev, TypeSafe, and
local LLMs. It turns unstructured model guesses into validated Noul, Choice,
and Score decisions with consensus, verification, calibration, abstention,
and CI gates.

[![Tests](https://github.com/aiwithenoch/Jev-Skill/actions/workflows/test.yml/badge.svg)](https://github.com/aiwithenoch/Jev-Skill/actions/workflows/test.yml)
[![ClawHub](https://img.shields.io/badge/ClawHub-Jev%20Skill-6f42c1)](https://clawhub.ai/aiwithenoch/skills/jev-skill)

Open-source repository: <https://github.com/aiwithenoch/Jev-Skill>

Built for developers shipping reliable AI agents, LLM routing, RAG systems,
structured extraction, model evaluation, and production automation.

For LangChain agents, Jev can sit in the control plane: route a run to a
cheaper or stronger model, classify a proposed tool call before execution, and
keep the final permission decision in code. See
[references/langchain.md](references/langchain.md) and the optional
[example](examples/langchain_jev.py).

## Transcript-derived control plane

The [LangChain “Building a Harness with Jev” video](https://youtu.be/VE5dsWll06M)
shows three practical control-plane jobs: route simple work to a cheaper model,
gate risky tool calls, and score agent traces against a rubric. The repository
now includes dependency-free policies for the last mile in
[`scripts/jev_control.py`](scripts/jev_control.py):

```python
from jev_control import assess_tool_call, judge_typed_answers, route_choice

route = route_choice(
    response,
    {"fast": "cheap-model", "strong": "strong-model"},
    question_id="complexity",
    min_confidence=0.80,
    min_margin=0.10,
)

gate = assess_tool_call(
    "delete_database",
    response,
    question_id="tool_risk",
    protected_tools={"delete_database"},
    authorized=policy_authorized,
)

grade = judge_typed_answers(response, rubric)
```

Routing uses the probability distribution and runner-up margin rather than a
self-reported confidence field. Protected tools fail closed on invalid or
missing classifier output, and a low risk score never grants authorization.
The rubric judge returns `accept`, `review`, or `reject`; it does not execute
the agent or hide uncertainty.

## Built by AI With Enoch

Jev Skill is created and maintained by Enoch Ansong, an AI engineer and
creator from Ghana, founder of Riverside AI and AI With Enoch. The project is
part of a wider mission to build practical, accessible AI systems and help
more people across Africa create with AI.

- Website: <https://aiwithenoch.com>
- GitHub: <https://github.com/aiwithenoch>
- LinkedIn: <https://www.linkedin.com/in/blacctbwoy>
- X/Twitter: <https://x.com/aiwithenoch>
- Instagram: <https://www.instagram.com/aiwithenoch>
- TikTok: <https://www.tiktok.com/@aiwithenoch>

## Join the community

Share benchmarks, adapters, golden cases, failure examples, and production
lessons through the [AI With Enoch community](https://github.com/aiwithenoch/aiwithenoch-community).
Community preview work also lives in
[ai-with-enoch-community](https://github.com/aiwithenoch/ai-with-enoch-community).
Issues and pull requests are welcome here—especially improvements that make
local AI more reliable and understandable.

## Why this exists

Most model integrations ask for prose and then hope the answer is correct.
That makes routing, grading, extraction, and automation fragile. Jev Skill
defines the decision explicitly, validates the shape of every response, tests
the model on reviewed cases, and escalates uncertainty instead of hiding it.

Jev Skill treats a model as a semantic decision layer: the application owns
schemas, thresholds, arithmetic, policy, side effects, and escalation. The
included harness lets the same Noul/Choice/Score question set run against:

- TypeSafe Jev (`POST /v1/systemone`)
- OpenJev's local TypeSafe-compatible server (`POST /v1/systemone`) backed by
  one-pass option scoring on Apple Silicon/MLX
- AlexWortega's openjev Hugging Face checkpoint through its SGLang
  `/classify` endpoint, with NLI logits adapted to typed decisions
- LocalJev's TypeScript/Bun bridge (`POST /v1/systemone`) backed by an
  OpenAI-compatible DiffusionGemma endpoint
- [Von](https://github.com/wfzyx/von), [LitJev](https://github.com/zhengxuyu/litjev),
  and [Simple-JEV](https://github.com/featherless-ai/simple-jev), each through
  its documented native `POST /v1/systemone` route
- Ollama native structured outputs (`POST /api/chat`)
- OpenAI-compatible local servers such as vLLM, LM Studio, and llama.cpp

The local path does not claim to turn a smaller checkpoint into Jev. It
reproduces the typed contract and adds strict validation, test-time consensus,
optional verification, explicit review/abstention, calibration, and CI gates.

## Quick start

Validate a question map and JSONL golden set without making a model call:

```bash
python3 scripts/jev_harness.py \
  --questions questions.json \
  --cases cases.jsonl \
  --validate-only
```

Run against Jev:

```bash
export TYPESAFE_API_KEY="..."
python3 scripts/jev_harness.py \
  --provider typesafe \
  --model jev-1.13.0 \
  --questions questions.json \
  --cases cases.jsonl \
  --output jev-report.json
```

Run against Ollama with a five-sample ensemble and verifier:

```bash
python3 scripts/jev_harness.py \
  --provider ollama \
  --base-url http://127.0.0.1:11434 \
  --model qwen3:8b \
  --samples 5 --temperature 0.4 --seed 17 --verify \
  --questions questions.json \
  --cases cases.jsonl \
  --output local-report.json
```

Run against vLLM, LM Studio, or llama.cpp server:

```bash
python3 scripts/jev_harness.py \
  --provider openai-compatible \
  --base-url http://127.0.0.1:8000/v1 \
  --model local-model \
  --samples 5 --temperature 0.4 --verify \
  --questions questions.json \
  --cases cases.jsonl
```

Run against the community [OpenJev](https://github.com/daseinlabs/open-jev)
server after its Apple-Silicon setup and `make serve`:

```bash
git clone https://github.com/daseinlabs/open-jev.git
cd open-jev
make setup
make serve
```

Then, from the Jev Skill repository, run:

```bash
python3 scripts/jev_harness.py \
  --provider openjev \
  --base-url http://127.0.0.1:8000 \
  --model jev-local \
  --questions questions.json \
  --cases cases.jsonl \
  --concurrency 1 \
  --output openjev-report.json
```

OpenJev is a community implementation, not TypeSafe's proprietary Jev
weights. Its native endpoint returns the same typed response surface, so this
repo can measure its accuracy, calibration, latency, and review rate beside
the hosted model without changing the question set. OpenJev's MLX scorer is
deterministic; repeated samples are useful for transport stability, not
sampling diversity.
OpenJev's default zero-shot log-probability scores are not automatically
calibrated; use a labeled golden set and the harness calibration metrics before
using thresholds in production.

For the open-weight [AlexWortega/openjev](https://huggingface.co/AlexWortega/openjev)
checkpoint, use the SGLang serving files published with the model card. The
small v2s checkpoint is a practical starting point; the 4B and 35B variants
need more hardware. This path requires an SGLang-compatible environment and
does not download weights into this repository:

```bash
hf download AlexWortega/openjev \
  --include "qwen3.5-0.8b-nli-v2s-long/*" "code/*" \
  --local-dir openjev_hf
cd openjev_hf/code
bash serve_sglang.sh ../qwen3.5-0.8b-nli-v2s-long 30000
```

Then run the harness against the raw SGLang classifier:

```bash
python3 scripts/jev_harness.py \
  --provider openjev-hf \
  --base-url http://127.0.0.1:30000 \
  --model qwen3.5-0.8b-nli-v2s-long \
  --concurrency 1 \
  --questions questions.json \
  --cases cases.jsonl \
  --output openjev-hf-report.json
```

This provider sends NLI premise/hypothesis pairs to `/classify`, converts
`contradiction / entailment / neutral` logits into Noul, Choice, and Score
answers, and emits a calibration warning. Those derived probabilities are not
the same as direct OpenJev or hosted Jev probabilities; benchmark them on a
labeled set before using thresholds. The checkpoint is MIT-licensed on its
model card; review upstream terms and hardware requirements before
redistributing weights.

For a portable DiffusionGemma bridge, run
[LocalJev](https://github.com/githubnext/localjev) on port `8080` after
connecting it to your local OpenAI-compatible inference server:

```bash
git clone https://github.com/githubnext/localjev.git
cd localjev
bun install
cp .env.example .env
# Configure LOCALJEV_UPSTREAM, LOCALJEV_UPSTREAM_MODEL, and its key if needed.
bun run start
```

Then evaluate it with the same golden set:

```bash
python3 scripts/jev_harness.py \
  --provider localjev \
  --base-url http://127.0.0.1:8080 \
  --model localjev-latest \
  --concurrency 2 \
  --questions questions.json \
  --cases cases.jsonl \
  --output localjev-report.json
```

LocalJev is wire-compatible but its probabilities are generated and
self-reported by the upstream model; they are not equivalent to reading
OpenJev logits. Treat its calibration as a separate benchmark result.

### More native System One runtimes

The same native adapter also supports the open-source `von`, `litjev`, and
`simple-jev` providers. The harness records each provider's protocol,
architecture, probability semantics, and calibration status in every report:

```bash
python3 scripts/jev_harness.py \
  --provider von --model von-latest --base-url http://127.0.0.1:8000 \
  --questions questions.json --cases cases.jsonl --output von-report.json

python3 scripts/jev_harness.py \
  --provider litjev --model litjev --base-url http://127.0.0.1:8000 \
  --questions questions.json --cases cases.jsonl --output litjev-report.json

python3 scripts/jev_harness.py \
  --provider simple-jev --model Qwen/Qwen3.5-2B \
  --base-url http://127.0.0.1:8000 \
  --questions questions.json --cases cases.jsonl --output simple-jev-report.json
```

These are transport-compatible, not model-equivalent. Von's repository
describes an Apache-2.0 native decision scorer; LitJev documents direct label
logits and says its probabilities are not calibrated by default; Simple-JEV
documents a next-token-logit classifier. Verify the exact upstream revision,
checkpoint, hardware, and calibration on your own golden set. See the full
[ecosystem map](references/ecosystem.md).

### Fit calibration instead of trusting confidence

Use a separate set tagged `calibration`, then apply the fitted profile to a
fresh run:

```bash
python3 scripts/jev_harness.py \
  --provider von --model von-latest \
  --questions questions.json --cases cases.jsonl --tag calibration \
  --output von-calibration-run.json

python3 scripts/fit_calibration.py von-calibration-run.json \
  --output von-temperature.json

python3 scripts/jev_harness.py \
  --provider von --model von-latest \
  --calibration-profile von-temperature.json \
  --questions questions.json --cases heldout-cases.jsonl \
  --output von-heldout.json
```

The fitter uses dependency-free temperature scaling over the typed
probabilities already exposed by the provider. It does not recover hidden
logits or make calibration transfer to a different model, domain, language,
option count, or quantization. The harness also rejects materially inconsistent
Score values instead of scoring a fabricated score against its distribution.

### Compare only matched reports

```bash
python3 scripts/compare_reports.py von-heldout.json litjev-heldout.json
```

The comparison tool refuses to mix reports with different question/case hashes
or tag filters, and exposes provider semantics beside accuracy, calibration,
review rate, warnings, and p95 latency.

## LangChain agent harness

The official `langchain-typesafe` integration exposes Jev as a LangChain
Runnable. Install it only in applications that need the optional integration:

```bash
python -m pip install "langchain-typesafe[experimental]"
```

Use `TypeSafeClassifier` for typed decisions. Its experimental middleware adds
two useful control points: `ModelRouterMiddleware` chooses a model once before
an agent run, and `AutoModeMiddleware` can block configured risky tools before
their handlers execute. These are learned signals, not authorization: keep
allowlists, user approval, path restrictions, spend caps, and side-effect
policy in deterministic application code. The middleware is fail-closed on
classifier errors in the current package, but tool safety still belongs to
the runtime.

The LangChain package calls hosted TypeSafe Jev. It does not automatically
switch to this repository's local `openjev`, `openjev-hf`, or `localjev`
providers; use the harness CLI to benchmark those providers separately. Read
[the LangChain guide](references/langchain.md) for routing, pre-tool gating,
local-provider boundaries, and agent-level evaluation.

Use `--structured-protocol llama.cpp` for llama.cpp's direct schema request
shape. Structured output is strict by default; `--allow-json-repair` is an
explicit diagnostic escape hatch and should remain off in CI.

## Question and case format

Questions are a JSON object. A Noul is a yes/no probability, a Choice selects
one criterion key, and a Score uses an ordered level list:

```json
{
  "urgent": {
    "type": "noul",
    "instructions": "Does this require urgent attention?"
  },
  "team": {
    "type": "choice",
    "instructions": "Which team should handle this?",
    "criteria": {
      "billing": "Charges and refunds",
      "technical": "Bugs and outages",
      "other": "None of the above"
    }
  },
  "severity": {
    "type": "score",
    "instructions": "How severe is this?",
    "criteria": ["Minor", "Material", "Critical"]
  }
}
```

Cases are JSONL. `expected` is optional for collection-only runs:

```json
{"id":"ticket-1","tags":["golden","billing"],"state":{"message":"I was charged twice."},"expected":{"urgent":true,"team":"billing","severity":{"level":1,"tolerance":0.5}}}
```

## Reliability stack

The harness composes the following layers without asking the model for a chain
of thought:

1. schema-constrained JSON where the provider supports it;
2. strict typed response validation, finite/range checks, normalized distributions,
   and Score/distribution integrity checks;
3. independent sample aggregation over typed distributions;
4. consensus measurement and review routing;
5. an optional second typed verifier over evidence and candidate answers;
6. golden, metamorphic, adversarial, boundary, and context-rot slices;
7. Brier/log loss, calibration, Wilson accuracy intervals, latency, retries,
   tokens, optional cost, and CI quality gates;
8. state-size and warning-rate guardrails for production runs.

Consensus or verifier support never silently changes the proposed answer. Low
support becomes `decision: "review"`; application code decides whether that
means a human, deterministic checker, or fallback model.

## Development

The harness has no third-party Python dependencies. Run the checks from the
repository root:

```bash
python3 -m unittest discover -s tests -v
python3 -m py_compile scripts/jev_harness.py scripts/jev_calibration.py scripts/fit_calibration.py scripts/compare_reports.py
python3 /Users/admin/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
```

The tests use local fake HTTP servers and never require a TypeSafe key or a
running model. Live model benchmarks should be run separately with sensitive
golden sets kept out of version control.

## FAQ

### Does Jev Skill require the Jev API?

No. It can run against OpenJev, Von, LitJev, Simple-JEV, LocalJev, Ollama,
vLLM, LM Studio, or llama.cpp server.
The Jev API gives you Jev's model; local providers give you the same typed
contract and reliability harness using the model you run.

### Does it make a local model as intelligent as Jev?

No. It cannot change model weights. It can run native open decision servers or
wrap another local model, then make the resulting decisions more structured,
testable, measurable, calibrated, and safer to deploy.

### Can Codex or Claude Code use it?

Yes. They can create question sets, generate golden cases, run the harness,
review reports, and help fix failures. LangChain applications can also use
the optional `langchain-typesafe` Runnable and middleware; the harness itself
does not depend on an interactive coding agent.

### What does “Noul / Choice / Score” mean?

Noul answers a yes/no question with a probability. Choice selects one named
category. Score returns a bounded, ordered level with a probability
distribution. Your application still owns the final policy and side effects.

## Roadmap

- Conformal/coverage-aware threshold selection for domain-specific costs.
- More provider adapters and reproducible local benchmark packs.
- Shared adversarial and metamorphic case libraries.
- First-class integrations for AI coding agents and CI platforms.

## Research and design notes

See [SKILL.md](SKILL.md), [references/harness.md](references/harness.md), and
[references/research-notes.md](references/research-notes.md), plus the
[ecosystem map](references/ecosystem.md). The notes link
the official TypeSafe docs, local structured-output APIs, evaluation
frameworks, self-consistency/verifier research, and calibration references.

## License

MIT-0. See [LICENSE](LICENSE).
