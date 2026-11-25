# Model routing evidence — 6 November 2026

Research snapshot, not a live fleet evaluation. Scores and API rates inform
policy but do not measure a subscription allowance, total mission cost or
prove that a model/effort is exposed through a particular OpenClaw transport.
The operator selected two editions and excluded Gemini Carbon.

## General capability and effort

Artificial Analysis Intelligence Index v5.0.1 contains nine evaluations. Do
not compare these scores with the older v4.3.2 or v5.0 snapshots in the launch
references. Output speed measures generation, not total completion time.
Benchmark cost includes the index's input/cache/reasoning/output accounting.

| Configuration | Index | USD/task | Minutes/task | Output tokens/s |
|---|---:|---:|---:|---:|
| [Sol high](https://artificialanalysis.ai/models/gpt-6-1-sol-high) | 50 | 0.59 | 7.0 | 53 |
| [Sol max](https://artificialanalysis.ai/models/gpt-6-1-sol) | 55 | 1.27 | 22.1 | 51 |
| [Terra high](https://artificialanalysis.ai/models/gpt-6-1-terra-high) | 42 | 0.26 | 4.0 | 70 |
| [Terra max](https://artificialanalysis.ai/models/gpt-6-1-terra) | 51 | 0.96 | 13.7 | 73 |
| [Astra medium](https://artificialanalysis.ai/models/gpt-6-astra-medium) | 52 | 2.73 | 6.5 | 46 |
| [Astra max](https://artificialanalysis.ai/models/gpt-6-astra) | 57 | 6.24 | 20.8 | 42 |
| [Luna high](https://artificialanalysis.ai/models/gpt-6-luna-high) | 21 | 0.07 | 5.8 | 95 |
| [Luna max](https://artificialanalysis.ai/models/gpt-6-luna) | 28 | 0.15 | 12.5 | 100 |
| [Opus 5.5 max](https://artificialanalysis.ai/models/claude-opus-5-5) | 59 | 10.04 | 26.7 | 108 |
| [Sonnet 5.5 max](https://artificialanalysis.ai/models/claude-sonnet-5-5) | 55 | 10.02 | 31.5 | 151 |
| [Haiku 5.5 max](https://artificialanalysis.ai/models/claude-haiku-5-5) | 36 | 0.41 | 15.7 | 239 |
| [Grok 4.7 xhigh](https://artificialanalysis.ai/models/grok-4-7) | 35 | 7.77 | 24.3 | 72 |
| [Argon high](https://artificialanalysis.ai/models/gemini-4-argon) | 50 | 9.95 | 26.9 | 72 |
| [Flash 3.8 high](https://artificialanalysis.ai/models/gemini-3-8-flash) | 31 | 7.77 | 14.6 | 113 |
| [Flash-Lite 3.5](https://artificialanalysis.ai/models/gemini-3-5-flash-lite) | 12 | 0.69 | 1.7 | 299 |

AA applies $4/$20 input/output rates to Argon. Google's introductory rate is
$2/$10 until November 30, then $4/$20. Preserve AA's reported cost rather than
silently presenting it as the current promotional bill.
[Google pricing announcement](https://cloud.google.com/blog/products/ai-machine-learning/gemini-4-argon-available-on-google-cloud).

## Coding and effort

[CursorBench 4.0](https://cursor.com/evals) tests ambiguous multi-file coding
tasks. These configurations run in Cursor's environment; their results do
not establish identical quality through another provider adapter.

| Configuration | Score | USD/task |
|---|---:|---:|
| Opus 5.5 medium | 52.5% | 2.91 |
| Opus 5.5 high | 56.0% | 3.97 |
| Opus 5.5 xhigh | 56.0% | 6.98 |
| Opus 5.5 max | 57.8% | 13.43 |
| Sonnet 5.5 high | 47.8% | 1.20 |
| Sonnet 5.5 xhigh | 53.1% | 2.81 |
| Sonnet 5.5 max | 55.5% | 7.05 |
| Haiku 5.5 high | 42.3% | 0.32 |
| Haiku 5.5 max | 48.4% | 1.12 |
| Argon medium | 52.8% | 4.39 |
| Argon high | 52.9% | 4.57 |
| Grok 4.7 high | 43.9% | 4.69 |
| Grok 4.7 xhigh | 46.3% | 6.01 |
| Composer 2.5 | 27.7% | 0.68 |

Opus high matches xhigh's rounded score here at lower cost. Argon medium and
high are nearly tied. Sonnet xhigh is a quality-oriented coding choice; high
remains suitable where the simpler task and latency warrant it. These are
workload-specific observations, not proof that the same effort wins all tasks.

The [public Terminal-Bench 4.0 leaderboard](https://www.tbench.ai/?efforts=all&version=4.0)
reports Opus max 64.8% ±3.1, Sonnet max 61.8% ±2.9, Astra max 58.2% ±2.8
and Sol 6.1 max 58.2% ±3.1. Claude Code and Codex harnesses differ.
[OpenAI separately reports](https://openai.com/index/introducing-gpt-6-1-terra/)
Terra max at 50.3%; keep vendor and leaderboard runs distinct.

[Composer's product page](https://cursor.com/composer) reports 69.3% on
Terminal-Bench 2.0 and 79.8% on SWE-bench Multilingual. These are different
evaluations from Terminal-Bench 4.0 and CursorBench 4.0. Composer's token
price alone does not establish a coding advantage over the other candidates.

## Vision and professional application work

[Roboflow Vision Evals](https://playground.roboflow.com/evals), evaluation
snapshot October 26 with pricing updated November 6, uses five tasks at its
provider-mapped low tier for the aggregate table. Older rows can still use
the prior single-run protocol. This is vision evaluation, not GUI completion.

| Model | Aggregate score | USD/sample | Seconds/sample |
|---|---:|---:|---:|
| Argon | 87.5% | 0.0058 | 13.40 |
| Terra 6.1 | 85.8% | 0.0033 | 10.05 |
| Astra | 83.4% | 0.034 | 9.94 |
| Opus 5.5 | 82.0% | 0.015 | 7.63 |
| Sol 6.1 | 81.7% | 0.0068 | 12.82 |
| Flash 3.8 | 79.8% | 0.0045 | 12.76 |
| Sonnet 5.5 | 77.6% | 0.0073 | 8.33 |
| Luna | 69.7% | 0.0004 | 10.21 |
| Haiku 5.5 | 69.6% | 0.0006 | 11.01 |
| Grok 4.7 | 63.5% | 0.020 | 33.31 |

Argon leads counting, OCR and reasoning; Terra leads detection. The older
[Terra effort comparison](gpt61-terra-20261028.md) remains relevant as a
dated vision protocol comparison, not an updated AA score.

[Mercor APEX-Agents](https://www.mercor.com/apex/apex-agents-leaderboard/)
reports Argon high 82.4% ±4.3, Sonnet max 75.5% ±4.7 and Opus max
73.5% ±4.9. Sonnet medium is 44.6% ±5.6 and Opus medium 52.5% ±5.6.
APEX includes reasoning and multiple applications; it is not exclusively
screenshot-driven GUI work. Its results support evaluating Argon for
professional application work but do not prove a universal default.

[Opus's launch report](https://www.anthropic.com/claude-opus-5-5) gives
OSWorld 2.1 partial scores of 81.8% for Opus and 80.1% for Sonnet. The
[Haiku report](https://www.anthropic.com/claude-haiku-5-5) gives offline
subset scores of 72.4% for Haiku and 83.9% for Sonnet. Do not combine
partial and offline-subset scores into one ranking.

## Model identity and controls

- [Current Claude family](https://www.anthropic.com/news/models): Opus,
  Sonnet and Haiku 5.5. Haiku's low-context token rate applies only up to
  100K prompt tokens; higher context has different rates.
- [Claude effort](https://platform.claude.com/docs/en/build-with-claude/effort):
  validate the actual model and adapter's supported effort controls.
- [Composer 2.5](https://cursor.com/docs/models/cursor-composer-2-5): adaptive
  calibration; do not manufacture OpenAI effort fields for it.
- [Grok 4.7](https://docs.x.ai/developers/model-capabilities/text/reasoning):
  low, medium, high and xhigh reasoning effort; high is the API default.
- [Gemini Pro 3.1 model card](https://deepmind.google/models/model-cards/gemini-3-1-pro/):
  Pro remains a distinct model; its older evaluations use a different model
  lineup. No current like-for-like v5.0.1 Pro score was recovered in this pass.
- [Google model migration guidance](https://github.com/google-gemini/gemini-skills/blob/main/skills/gemini-api-dev/references/migration.md)
  identifies Flash 3.8 and Flash-Lite 3.5; use the native thinking-level
  interface supported by the model/transport.
- [Flash-Lite model documentation](https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash-lite)
  lists tool use and thinking support. That does not establish the exact
  controls exposed by a subscription adapter.

The new edition's defaults are policy choices. Live provider invocation,
subscription billing, parameter forwarding and a common real-task model
comparison remain separate acceptance checks on each target runtime.
