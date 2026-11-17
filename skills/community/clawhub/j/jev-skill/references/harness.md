# Jev evaluation harness

`scripts/jev_harness.py` is a small, dependency-free runner for Jev golden
sets. It validates typed question definitions, calls TypeSafe, OpenJev, Von,
LitJev, Simple-JEV, LocalJev, or a local Ollama/OpenAI-compatible endpoint
concurrently, and reports accuracy, calibration, reliability, latency, and
token usage. It does not print state or API keys.

## Input files

Questions are a JSON object:

```json
{
  "urgent": {
    "type": "noul",
    "instructions": "Does this message require urgent attention?"
  },
  "team": {
    "type": "choice",
    "instructions": "Which team should handle this?",
    "criteria": {
      "billing": "Charges or refunds",
      "technical": "Bugs or integration failures",
      "other": "None of the above"
    }
  },
  "severity": {
    "type": "score",
    "instructions": "How severe is the issue?",
    "criteria": ["Minor", "Material", "Critical"]
  }
}
```

Cases are JSONL. `expected` is optional for collection-only runs; include it
for accuracy:

```json
{"id":"ticket-1","tags":["golden","billing"],"state":{"message":"I was charged twice.","tier":"pro"},"expected":{"urgent":true,"team":"billing","severity":{"level":1,"tolerance":0.5}}}
```

Expected Noul values are booleans or `0`/`1`; Choice values are option keys;
Score values are numeric levels. A Score may also use
`{"level": 1, "tolerance": 0.5}` for a case-specific tolerance. The harness
treats a Noul probability of at least `0.5` as the predicted yes/no label and
reports the raw probability too. For Choice and Score it reports the returned
confidence. These are evaluation defaults, not universal production
thresholds. `tags` is optional and is intended for slices such as `golden`,
`metamorphic`, `adversarial`, `numeric`, `date-time`, or `context-rot`.

## Run it

Validate without a key:

```bash
python3 scripts/jev_harness.py \
  --questions questions.json \
  --cases cases.jsonl \
  --validate-only
```

Run against Jev:

```bash
export TYPESAFE_API_KEY='…'
python3 scripts/jev_harness.py \
  --questions questions.json \
  --cases cases.jsonl \
  --output jev-report.json \
  --concurrency 4
```

Run the same typed contract against a local Ollama model:

```bash
python3 scripts/jev_harness.py \
  --provider ollama \
  --base-url http://127.0.0.1:11434 \
  --model qwen3:8b \
  --samples 5 --temperature 0.4 --seed 17 --verify \
  --questions questions.json --cases cases.jsonl \
  --output ollama-report.json
```

Run against vLLM, LM Studio, or llama.cpp server through its
OpenAI-compatible endpoint:

```bash
python3 scripts/jev_harness.py \
  --provider openai-compatible \
  --base-url http://127.0.0.1:8000/v1 \
  --model local-model \
  --samples 5 --temperature 0.4 --verify \
  --questions questions.json --cases cases.jsonl
```

Run against the community OpenJev server. OpenJev exposes the native typed
route, so the harness sends the same `state`, `model`, and `questions` payload
without a generated JSON wrapper:

```bash
python3 scripts/jev_harness.py \
  --provider openjev \
  --base-url http://127.0.0.1:8000 \
  --model jev-local \
  --concurrency 1 \
  --questions questions.json --cases cases.jsonl \
  --output openjev-report.json
```

The current OpenJev implementation is a local MLX/Apple-Silicon scorer with a
TypeSafe-compatible `/v1/systemone` surface. It is not TypeSafe's hosted Jev
weights. Its scorer is deterministic, so non-zero temperature and per-sample
seed flags do not create independent model samples; use repeated calls only
when measuring endpoint stability.
The upstream zero-shot scorer also documents its probabilities as approximate,
so calibrate thresholds on your own labeled cases rather than treating a high
local probability as proof.

Run the open-weight [AlexWortega/openjev](https://huggingface.co/AlexWortega/openjev)
checkpoint through its published SGLang `/classify` server:

```bash
python3 scripts/jev_harness.py \
  --provider openjev-hf \
  --base-url http://127.0.0.1:30000 \
  --model qwen3.5-0.8b-nli-v2s-long \
  --concurrency 1 \
  --questions questions.json --cases cases.jsonl \
  --output openjev-hf-report.json
```

The server returns raw three-class NLI logits in each `embedding` field. The
harness applies softmax, uses entailment scores to rerank Choice/Score options,
and maps a Noul to `entailment + 0.5 * neutral`. It warns on every request so
reports cannot silently present these derived values as direct Jev
probabilities. The model card publishes 0.8B, 4B, and 35B-A3B variants and an
MIT license; download and hardware setup remain the operator's responsibility.
Use the same golden set and keep this provider's calibration slices separate
from native OpenJev and hosted TypeSafe results.

Run against [LocalJev](https://github.com/githubnext/localjev), the MIT-licensed
Bun bridge for OpenAI-compatible DiffusionGemma servers:

```bash
python3 scripts/jev_harness.py \
  --provider localjev \
  --base-url http://127.0.0.1:8080 \
  --model localjev-latest \
  --concurrency 2 \
  --questions questions.json --cases cases.jsonl \
  --output localjev-report.json
```

LocalJev returns the native typed wire shape, but its probabilities come from
the upstream model's prompted JSON distribution rather than direct option
logits. Keep it as a separate provider in comparisons and calibrate it on the
same labeled cases. Its own queue and in-flight limits should be respected;
start with `--concurrency 1` or `2`.

The native adapter also accepts `--provider von`, `--provider litjev`, and
`--provider simple-jev`. Their documented defaults are all port `8000`; pass
the model identifier loaded by the server:

```bash
python3 scripts/jev_harness.py \
  --provider von --model von-latest \
  --base-url http://127.0.0.1:8000 \
  --questions questions.json --cases cases.jsonl
```

The reports intentionally label these providers differently. Von is a native
decision scorer, LitJev uses direct label logits, and Simple-JEV uses next-token
logits. Transport compatibility is not probability or accuracy parity. See
the [ecosystem map](ecosystem.md) for licenses, upstream claims, and the
in-process Laya/poorjev/NanoJev projects that need custom adapters.

For llama.cpp's direct JSON-schema request shape, add
`--structured-protocol llama.cpp`. Local API keys are optional; if a server
requires one, put it in the environment variable named by `--api-key-env`
(default `LOCAL_MODEL_API_KEY`). This reproduces Jev's typed decision
contract and adds a measured reliability layer around a local model; it does
not make a smaller model equivalent to Jev. Keep a Jev run as the reference
benchmark and compare local models on the same cases.

Local reliability controls:

- `--samples N` makes independent calls and averages typed distributions. For
  `Choice` it chooses the highest mean probability; for `Score` it uses the
  probability-weighted expected level; for `Noul` it averages the yes
  probability.
- `--min-valid-samples` sets the minimum usable sample count. The default is
  all requested samples, so a malformed or failed sample fails the case.
- `--consensus-threshold` marks low agreement as `decision: "review"`.
  `--max-review-rate` can fail the complete run when too many cases abstain.
- `--verify` sends the proposed typed answers and original evidence through a
  second typed Noul pass. Any verifier probability below `--verify-threshold`
  marks the case for review; it never changes the candidate answer.
- Schema-constrained output is on by default. `--no-structured-output` is an
  escape hatch for servers without grammar support. Keep
  `--allow-json-repair` off in CI and only enable it when you want to measure
  wrapper text around otherwise valid JSON.
- `--seed` increments the seed per sample. A non-zero `--temperature` is
  normally needed for useful ensemble diversity; the harness warns when an
  ensemble is run at temperature zero.
- `--max-state-bytes` fails oversized serialized state before a model call,
  providing a simple context and privacy guardrail.
- `--max-warning-rate` fails CI when too many cases emit non-fatal warnings,
  such as missing usage or explicitly enabled JSON repair.

### Calibration profiles

Fit temperature scaling on a separate labeled slice. The default fitter uses
cases tagged `calibration` and requires 20 answers per primitive so a profile
is not silently created from a handful of examples:

```bash
python3 scripts/fit_calibration.py calibration-run.json \
  --output temperature-profile.json

python3 scripts/jev_harness.py \
  --provider von --model von-latest \
  --calibration-profile temperature-profile.json \
  --questions questions.json --cases heldout-cases.jsonl \
  --output heldout-report.json
```

The profile stores only fitting metadata and temperatures. Temperature scaling
recomputes Noul probabilities and Choice/Score distributions, then recomputes
the selected answer and Score expectation. It does not recover hidden logits;
refit after changing provider, checkpoint, domain, language, quantization, or
option cardinality. Use `--by-question` only when each question has enough
calibration examples.

Compare matched reports with:

```bash
python3 scripts/compare_reports.py report-a.json report-b.json
```

The comparator refuses different question/case hashes or tag filters unless
`--allow-mismatch` is explicitly supplied.

For a reproducible benchmark, pin the resolved model version; use the alias
for a moving canary:

```bash
python3 scripts/jev_harness.py --questions questions.json --cases cases.jsonl \
  --model jev-1.13.0 --tag golden
```

Useful CI/evaluation controls:

```bash
python3 scripts/jev_harness.py \
  --questions questions.json \
  --cases cases.jsonl \
  --min-accuracy 0.90 \
  --max-error-rate 0 \
  --max-noul-brier 0.12 \
  --max-score-mae 0.40 \
  --input-price-per-million 0.042 \
  --output-price-per-million 0
```

The command exits non-zero when a case fails, a response is malformed, or a
requested gate fails. `--offset`, `--limit`, repeated `--case-id`, and repeated
`--tag` support shards and targeted debugging; all supplied tags must be
present on a selected case. `--noul-threshold` and `--score-tolerance` control
evaluation policy without changing the questions. Pricing is always opt-in so
stale provider pricing is never silently assumed.

The runner validates the documented response contract before scoring: every
question must have a matching typed answer; Choice probabilities must cover
the criteria; Score legends and probability keys must cover every level; all
probabilities, confidence values, scores, and token counts must be finite and
in range. It reports Noul accuracy, Brier score, log loss, reliability/ECE,
precision/recall/F1 and a confusion matrix; Choice accuracy, confidence and confusion; Score level
accuracy, tolerance hit rate, MAE and RMSE; expected calibration error and
confidence-threshold selective coverage; per-question and per-tag slices; plus
mean/p50/p95 latency, state byte sizes, retry attempts, resolved model IDs,
request IDs, and token totals. Provider architecture, probability semantics,
and calibration status are recorded alongside the metrics. Missing usage is recorded as a warning, not a
false response failure, because the SDK response surface allows usage to be
absent. The summary also includes Wilson 95% accuracy intervals, provider and
sample counts, ensemble agreement, verifier support, and the fraction of
successful cases marked for review.

It retries transient `408`, `429`, `500`, `502`, `503`, `504`, and `529`
responses with bounded full-jitter backoff, honoring `Retry-After` when
present. The API key and input state are never written to the report. Keep
golden sets and reports out of source control when they contain customer or
other sensitive data. Use representative, adversarial cases and compare Jev
with the existing model or rule-based baseline before shipping thresholds.

## Build the strongest suite

Do not rely on a large random sample alone. Keep a small, reviewed suite for
each known jaggedness family: literal and indirect references, arithmetic and
numeric formats, dates/time zones, contradictory or prompt-injected content,
missing evidence, structural invariants, and large irrelevant context. Add
metamorphic variants that reorder irrelevant fields or add distractors while
preserving the label. Require a safe escalation label at uncertainty
boundaries, then gate aggregate and tagged-slice metrics in CI. For production
thresholds, prefer a pinned model benchmark plus a separate `jev-latest`
canary so model alias movement cannot silently change the release decision.
