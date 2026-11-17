# Jev-class ecosystem map

Research snapshot: 2026-09-22. This is an interoperability map, not a
leaderboard. A shared JSON contract does not make two models' probabilities,
latency, weights, or licenses equivalent. Re-run the harness on the exact
checkpoint, runtime, quantization, hardware, and question set you plan to ship.

## Provider matrix

| Provider/project | Route or API | What the number means | Harness path | Important caveat |
| --- | --- | --- | --- | --- |
| [TypeSafe Jev](https://docs.typesafe.ai/api.md) | Hosted `POST /v1/systemone` | Provider-native Jev signal | `typesafe` | Hosted model; pin a model for reproducible comparisons. |
| [daseinlabs/open-jev](https://github.com/daseinlabs/open-jev) | Native `POST /v1/systemone` | Local scorer output | `openjev` | Independent community implementation; verify checkpoint and calibration separately. |
| [Von](https://github.com/wfzyx/von) | Native `POST /v1/systemone` | Native decision-scorer output | `von` | Apache-2.0 source; upstream benchmark/calibration claims are not independently verified by this repository. |
| [LitJev](https://github.com/zhengxuyu/litjev) | Native `POST /v1/systemone` | Direct label-logit probabilities | `litjev` | Apache-2.0 original code; upstream states probabilities are not calibrated by default. |
| [Simple-JEV](https://github.com/featherless-ai/simple-jev) | Native `POST /v1/systemone` alias of `/v1/classifier` | Next-token-logit probabilities | `simple-jev` | Apache-2.0 source; token-boundary and model-template constraints apply. |
| [LocalJev](https://github.com/githubnext/localjev) | Native `POST /v1/systemone` | Prompted/self-reported JSON probabilities | `localjev` | MIT bridge; do not compare its confidence directly with a logit-reading model. |
| [AlexWortega/openjev](https://huggingface.co/AlexWortega/openjev) | SGLang `POST /classify` | NLI-derived probabilities | `openjev-hf` | Separate open-weight NLI model; the adapter maps contradiction/entailment/neutral into typed answers. |
| [Laya](https://github.com/NandhaKishorM/laya) | In-process Python API | Laya checkpoint output | via Simple-JEV's Laya backend or a custom adapter | Apache-2.0; the upstream Python package is not itself a stable HTTP provider in this harness. |
| [poorjev](https://github.com/rupeshpoojary9/poorjev) | In-process Python/MCP APIs | Calibrated local primitive output | custom adapter | MIT; useful calibration ideas, but its API is not the harness's native `/v1/systemone` transport. |
| [NanoJev](https://github.com/TianyuCodings/NanoJev) | Custom `/api/evaluate` service | Game/task-specific parallel decisions | custom adapter | MIT; its published results focus on navigation/game tasks and are not interchangeable with general typed decisions. |

The `von`, `litjev`, and `simple-jev` adapters were added because their
repositories document the same native route. They share transport code, but
the report records distinct `architecture`, `probability_semantics`, and
`calibration_status` metadata so an aggregate score cannot hide the difference.

## Fair comparison protocol

1. Freeze one question JSON file and one JSONL case file. The harness report
   records hashes for both the question definitions and the complete selected
   case manifest (including state and labels, without printing them).
2. Pin the model/checkpoint revision, runtime version, quantization, device,
   batch/concurrency, and server flags. A provider alias such as `latest` is a
   canary, not a reproducible experiment.
3. Keep calibration data separate from test data. Fit a profile with
   `scripts/fit_calibration.py` on a calibration-tagged split, then apply that
   profile to a fresh evaluation run.
4. Report exact accuracy with uncertainty, Noul Brier/log loss/ECE, Choice/Score
   confidence ECE, Score MAE, review rate, warning rate, p95 latency, token
   usage, and cost when a real tariff exists. Never turn missing usage into a
   zero cost.
5. Measure cold start and warm inference separately. Native one-pass scorers,
   prompted bridges, and autoregressive JSON wrappers have different startup
   and throughput behavior.
6. Add tagged adversarial, metamorphic, boundary, context-rot, and
   high-cardinality cases. A model that wins an average can still fail a
   critical slice.
7. Use `scripts/compare_reports.py` only after the input hashes match. If the
   hashes differ, the tool refuses the comparison unless `--allow-mismatch`
   is explicitly supplied.

## Calibration workflow

```bash
# 1. Run a labeled calibration split with the deployment provider.
python3 scripts/jev_harness.py \
  --provider von --model von-latest \
  --questions questions.json --cases cases.jsonl \
  --tag calibration --output von-calibration-run.json

# 2. Fit only the calibration-tagged answers. Twenty is the default minimum
#    per primitive; lower it only when the small-sample tradeoff is deliberate.
python3 scripts/fit_calibration.py von-calibration-run.json \
  --output von-temperature.json

# 3. Apply the profile on a new, untouched evaluation set.
python3 scripts/jev_harness.py \
  --provider von --model von-latest \
  --calibration-profile von-temperature.json \
  --questions questions.json --cases heldout-cases.jsonl \
  --output von-heldout.json
```

The fitter scales the typed probabilities already exposed by the provider. It
does not recover hidden logits or guarantee calibration transfer across a new
domain, question wording, option count, language, model revision, or
quantization. Treat a profile as deployment configuration and replace it when
those inputs change.

## Research leads worth keeping separate

- [JevBench](https://github.com/fstandhartinger/jevbench) is useful for its
  explicit separation of intelligence, calibration, speed, and cost. Do not
  copy its task text or labels into this repository; its own README says the
  task set is not ours to redistribute.
- [poorjev calibration](https://github.com/rupeshpoojary9/poorjev) is a useful
  reference for temperature scaling and selective prediction, but its claims
  are measured on its own evaluation set.
- [LitJev calibration docs](https://github.com/zhengxuyu/litjev/blob/main/docs/how-it-works.md)
  and [Laya benchmarks](https://github.com/NandhaKishorM/laya/blob/main/BENCHMARKS.md)
  reinforce the same rule: fit on held-out data and re-check high-cardinality
  choices rather than trusting a generic confidence field.
- [OpenLayer jevals](https://github.com/openlayer-ai/jevals) is a useful
  direction for agent traces and guardrails. A classifier remains a signal;
  authorization, tool allowlists, user approval, and side-effect policy stay
  deterministic.

