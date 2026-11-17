# ModelShow (`mdls`)

**Double-blind evaluation for AI models — ask once, compare every answer.**

ModelShow sends your prompt to several models in parallel, strips the names off their responses, and has an independent judge model rank them. The judge never knows which model wrote what, so the ranking reflects answer quality — not name recognition.

Ask a question with `mdls` in front of it and get back a scored, ranked comparison with the judge's commentary on each response.

---

## Installation

ModelShow is published on ClawHub (the public skill registry for OpenClaw) at **[clawhub.ai/schbz/skills/modelshow](https://clawhub.ai/schbz/skills/modelshow)**:

```bash
clawhub install modelshow
```

Or clone this repo into your managed skills directory:

```bash
git clone https://github.com/schbz/modelshow.git ~/.openclaw/skills/modelshow
```

Start a new OpenClaw session after installing so the skill is picked up.

To update later:

```bash
clawhub update modelshow
```

---

## Setup: Choose Your Models

ModelShow ships with a default model list in `config.json`, but the aliases need to match what's actually available on your instance. The easiest way to set this up is to ask your agent:

> *"List all available models on my instance with their labels, then update the ModelShow config at `~/.openclaw/skills/modelshow/config.json` with the models I want to compare."*

Your agent can inspect what's available, let you pick, and write the config for you.

Two settings matter most:

- **`models`** — the aliases that receive your prompt in parallel. More models means a richer comparison but a slower, costlier run.
- **`judgeModel`** — the model that performs the blind evaluation. For the cleanest results, pick one that isn't in your `models` list — though judging its own (anonymized) output is still fair, since the judge can't tell which response is its own.

The full option list is under [Configuration](#configuration-configjson).

---

## Quick Start

```
mdls your question here
```

> `modelshow` also works as the trigger keyword — the two are identical.

A run looks like this:

```
mdls explain the difference between TCP and UDP in plain English
```

```
🕶️ Double-Blind Judging Results:

🏆 grok (Score: 9.1/10)
[grok's full response]
Judge's assessment: Clear analogy, accurate, well-structured.

🥈 sonnet (Score: 8.4/10)
[sonnet's full response]
Judge's assessment: Thorough but slightly verbose for the target audience.

🥉 gemini (Score: 7.8/10)
[gemini's full response]
Judge's assessment: Accurate, missing a concrete example.
```

Every run is also saved to `config.outputDir` (default: `~/.openclaw/workspace/modelshow-results`) as both Markdown and JSON, so you can browse past comparisons or feed them into your own tools.

**Compare a specific lineup for one run** by listing aliases in brackets:

```
mdls [grok,kimi,sonnet] how does compound interest work
```

---

## How It Works

1. **Parallel inference** — your prompt goes to all configured models at once. Each responds independently, with no knowledge of the others or of being compared.
2. **Anonymization** — responses are stripped of model identity and assigned neutral labels (Response A, B, C...). Label order is shuffled with cryptographically secure randomization (`secrets.SystemRandom()`), so position reveals nothing.
3. **Blind judging** — a judge model evaluates the anonymized responses on accuracy, clarity, completeness, and usefulness (configurable). It scores each response, then writes an "Overall Assessment" of patterns across all of them.
4. **De-anonymization** — the label→model mapping is applied in reverse, restoring real names next to scores and commentary.
5. **Ranking** — results are ordered by the judge's scores and presented with full response text and per-model commentary.

The judging is double-blind in the practical sense: the models don't know they're competing, and the judge doesn't know who it's scoring.

---

## Why Blind?

Model names carry reputations, and reputations bias judgment — human or machine. A judge that can see names will tend to score the famous model's answer higher and scrutinize the underdog harder. Hiding identities forces the ranking to stand on the answers alone. The shuffle matters too: without it, a judge that habitually favors "Response A" would consistently favor whichever model happened to land there.

---

## Use Cases

**Fact checking** — compare how models handle accuracy, sourcing, and hedging on the same question. Overconfident wrong answers stand out quickly when set against more careful ones.
```
mdls does searing meat really seal in the juices?
```

**Creative work** — the same brief produces genuinely different tones, styles, and angles. Useful for inspiration or for finding the voice that fits your project.
```
mdls write a short poem about working late at night
```

**Technical decisions** — models often disagree about architecture and trade-offs, and seeing where they agree (or don't) is itself a signal.
```
mdls pros and cons of event sourcing vs traditional CRUD
```

**Code review** — different models catch different issues: one spots the performance problem, another the security concern, another the readability nit.
```
mdls review this Python function for potential issues: [paste code]
```

**Brainstorming** — when you want range rather than one "best" answer, several models naturally produce more diverse suggestions than repeated calls to one.
```
mdls give me 5 creative names for a productivity app for developers
```

---

## Security

ModelShow treats model output as untrusted data end-to-end:

- **No network access** — all bundled scripts are Python standard library only; they never open sockets or fetch URLs. Model queries go through your agent platform, not these scripts.
- **No shell exposure** — response and judge text is passed to scripts via files/stdin (`--file`), parsed strictly as JSON, and never placed on a shell command line or executed.
- **Prompt-injection defenses** — blind responses are wrapped in explicit delimiters and the judge is instructed to ignore any instructions embedded in them; manipulation attempts count against a response's score. The orchestrator never follows URLs found inside model output.
- **Constrained writes** — results are written only inside `outputDir` (sanitized filenames + traversal guard, no overwrites); temp payloads use unique per-run names; index pruning only touches ModelShow-pattern files.
- **Minimal reads** — scripts read the payload they're given, `config.json`, and (solely to map aliases to full model names) `~/.openclaw/openclaw.json`; nothing read is logged or transmitted.
- **Bounded inputs** — payloads over 64 MB are rejected with a clean JSON error.

---

## Configuration (`config.json`)

| Key | Description | Default |
|-----|-------------|---------|
| `keyword` | Trigger keyword | `"mdls"` |
| `models` | Model aliases to query in parallel | `["pro", "sonnet", "deepseek", "gpt4", "grok", "kimi"]` |
| `judgeModel` | Model used for blind judging | `"sonnet"` |
| `judgeCriteria` | Criteria the judge scores against | `["accuracy", "clarity", "completeness", "usefulness"]` |
| `judgeThinking` | Thinking-effort hint for the judge agent | `"medium"` |
| `systemPrompt` | System prompt prepended to each model's task | helpful-assistant default |
| `outputDir` | Where result files are saved | `"~/.openclaw/workspace/modelshow-results"` |
| `timeoutSeconds` | Max wait per model | `360` |
| `minSuccessful` | Minimum responses needed to proceed to judging | `2` |
| `parallel` | Query models in parallel or sequentially | `true` |
| `showTopN` | Number of top results to display | `10` |
| `includeResponseText` | Include full response text in output | `true` |
| `blindJudging` | Anonymize responses before judging | `true` |
| `blindJudgingLabels` | Label style for anonymization | `"alphabetic"` |
| `shuffleBlindOrder` | Randomize response order before judging | `true` |
| `includeAnonymizationKey` | Keep the blind-judging key in saved results (audit trail) | `true` |

---

## Scripts

| Script | Role |
|--------|------|
| `judge_pipeline.py` | Core pipeline: `anonymize` (label + shuffle responses) and `finalize` (de-anonymize judge output, extract rankings). Also `--selftest` for a zero-setup round-trip check. |
| `save_results.py` | Saves each run to `outputDir` as Markdown + JSON, resolving aliases to full model names and extracting the judge's Overall Assessment. Runs automatically after every comparison. |
| `update_modelshow_index.py` | Optional: builds a JSON index of results for a custom dashboard or static site. Not part of the core workflow. |
| `blind_judge_manager.py` | Deprecated compatibility shim — `judge_pipeline.py` is canonical. |
| `test_modelshow.py` | Test suite: `python3 -m unittest test_modelshow -v` (30 tests, stdlib-only). |

---

## Quick Test

> Paths assume a managed install (`~/.openclaw/skills/modelshow/`). If you installed elsewhere, substitute your skill path.

```bash
# Zero-setup round-trip check:
python3 ~/.openclaw/skills/modelshow/judge_pipeline.py --selftest
# → {"selftest": "pass", ...}

# Phase 1: Anonymize — write the payload to a file, then pass --file (never echo untrusted text)
printf '%s' '{"action":"anonymize","responses":{"sonnet":"Paris is the capital of France.","grok":"The capital of France is Paris, founded by the Parisii tribe."}}' > /tmp/anon.json
python3 ~/.openclaw/skills/modelshow/judge_pipeline.py --file /tmp/anon.json

# Phase 2: Finalize (use anonymization_map from Phase 1; include structured scores)
cat > /tmp/finalize.json <<'JSON'
{
  "action": "finalize",
  "judge_output": "1st: Response A — Score: 8.5/10\nClear and direct.\n\n2nd: Response B — Score: 7/10\nMore detailed but slightly verbose.",
  "anonymization_map": {"Response A": "grok", "Response B": "sonnet"},
  "scores": {"Response A": 8.5, "Response B": 7.0}
}
JSON
python3 ~/.openclaw/skills/modelshow/judge_pipeline.py --file /tmp/finalize.json
```

Expected Phase 2 output:
```json
{
  "deanonymized_judge_output": "1st: **grok** — Score: 8.5/10\nClear and direct.\n\n2nd: **sonnet** — Score: 7/10\nMore detailed but slightly verbose.",
  "ranked_models_deanonymized": [
    {"placeholder": "Response A", "model": "grok", "score": 8.5, "rank": 1},
    {"placeholder": "Response B", "model": "sonnet", "score": 7.0, "rank": 2}
  ],
  "ranking_source": "structured",
  "deanonymization_complete": true,
  "remaining_placeholders": []
}
```

---

## File Structure

```
modelshow/
├── SKILL.md                  — Orchestrator workflow instructions
├── config.json               — Models, judge, timeout, keyword settings
├── judge_pipeline.py         — Anonymize + finalize pipeline
├── save_results.py           — Saves results as Markdown + JSON
├── update_modelshow_index.py — Optional results indexer
├── blind_judge_manager.py    — Deprecated compatibility shim
├── test_modelshow.py         — Test suite
├── CHANGELOG.md              — Version history
└── README.md                 — This file
```

---

## Version History

See [CHANGELOG.md](CHANGELOG.md). Current release: **v1.2.0** — security hardening (unique per-run temp files, injection-resistant judge prompt, clean JSON error handling, 30-test suite).

## License

MIT — see [LICENSE](LICENSE).
