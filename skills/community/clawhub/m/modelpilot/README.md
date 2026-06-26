# ModelPilot

ModelPilot is a local-only skill for testing, comparing, promoting, replacing,
and cleaning up Ollama models.

It is built around a simple rule: a model should not replace an existing workflow
model after one good run. Run the same fixed prompt set twice, review both rounds,
then decide.

## What It Helps With

- Compare local Ollama models on real tasks
- Verify whether a `nothink` model actually suppresses thinking traces
- Decide whether a candidate model can replace a current model
- Produce compact benchmark reports
- Audit models before cleanup without deleting anything automatically

## Directory Layout

```text
modelpilot/
  SKILL.md
  README.md
  scripts/
  examples/
  tests/
  outputs/
```

## Safety Defaults

- Local Ollama only
- No cloud model APIs
- No uploads
- No model downloads
- No dependency installation
- No automatic model deletion
- Fictional examples only

## Basic Usage

Prepare a fictional prompt set:

```bash
python scripts/modelpilot_benchmark.py \
  --models llama3.2:latest qwen3:latest \
  --prompts examples/prompts.example.json \
  --rounds 2 \
  --output outputs/benchmark_results.json
```

Create a Markdown report:

```bash
python scripts/modelpilot_report.py \
  --input outputs/benchmark_results.json \
  --output outputs/benchmark_report.md
```

The scripts use Python standard library only. The benchmark script calls the local
`ollama` command and expects the models to already be installed.

## Replacement Rule

A model can be considered replacement-ready only after two independent rounds using
the same fixed prompt set.

Round 1 checks:

- the model runs
- response speed is acceptable
- output format is stable
- no-think behavior does not leak reasoning text

Round 2 checks:

- the same tasks still pass
- failure modes do not repeat
- quality is consistent enough for the target workflow

If either round fails on structured output, no-think behavior, or the user's core
task, keep the existing model.

## Example Decision Labels

- `replace_ready`: both rounds pass and manual review confirms quality
- `observe`: usable, but has minor instability or incomplete evidence
- `candidate_only`: only one round is complete
- `not_recommended`: repeated failures, output pollution, or unsafe automation fit

## Limits

ModelPilot does not prove general intelligence or leaderboard quality. It helps make
local workflow decisions based on fixed tasks, repeatability, and clean output.

The report script can detect mechanical issues, but semantic quality still needs a
human review.

