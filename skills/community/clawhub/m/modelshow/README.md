# ModelShow (`mdls`)

**Double-blind multi-model evaluation for AI responses.**

Query multiple models in parallel, anonymize their outputs, and let an independent judge rank them purely on merit — no model names, no reputation bias, just answer quality. Trigger with `mdls` (or `modelshow`).

---

## Installation

Install from [ClawHub](https://clawhub.ai) (the public skill registry for OpenClaw):

```bash
clawhub install modelshow
```

Or, if you prefer a manual install, clone this repo into your managed skills directory:

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

ModelShow ships with a default set of models in `config.json`, but you should tailor it to the models available on your instance. The easiest way to do this is to ask your agent:

> *"List all available models on my instance with their labels, then update the ModelShow config at `~/.openclaw/skills/modelshow/config.json` with the models I want to compare."*

Your agent can inspect what's available, let you pick which models to include, and write the config for you.

A few things to keep in mind:

- **`models`** — the list of model aliases that will receive your prompt in parallel. Add or remove entries to match your setup.
- **`judgeModel`** — the model that performs the double-blind evaluation. For unbiased results, pick a model that is *not* in your `models` list (though it will still work if it is — the judge never sees its own label).
- See the [Configuration](#configuration-configjson) table below for every available option.

---

## Quick Start

```
mdls your question here
```

> You can also use `modelshow` as the keyword — both work identically.

ModelShow will:
1. Send your prompt to every configured model via parallel inference
2. Collect all responses automatically (no manual polling needed)
3. Anonymize the responses and submit them for double-blind judging
4. De-anonymize and produce a merit-based ranking
5. Present a formatted comparison with scores and the judge's commentary
6. Save results to `config.outputDir` (default: `~/.openclaw/workspace/modelshow-results`) in both Markdown and JSON via `save_results.py`. The JSON includes full model names and a holistic "Overall Assessment" for use in your own tools or dashboards.

**Full example:**

```
mdls explain the difference between TCP and UDP in plain English
```

Output looks like:

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

---

## How It Works

ModelShow uses a double-blind evaluation protocol — the judge never knows which model wrote which response, and the models have no knowledge that they are being compared.

1. **Parallel inference** — Your prompt is sent to all configured models at the same time. Each model responds independently with no awareness of the others.
2. **Anonymization** — Responses are stripped of model identity and assigned neutral labels (Response A, Response B, Response C...). The mapping is shuffled using cryptographically secure randomization (`secrets.SystemRandom()`) so label order reveals nothing.
3. **Double-blind judging** — An independent judge model evaluates the anonymized responses on accuracy, clarity, completeness, and usefulness. It sees only the neutral labels and has no way to identify the source of any response. The judge provides both per-model rankings and a holistic "Overall Assessment" analyzing cross-model patterns.
4. **De-anonymization** — After the judge submits its evaluation, the anonymization map is applied in reverse to restore real model names alongside scores and commentary.
5. **Merit-based ranking** — The final output ranks models purely by the quality of their responses, free from name recognition or reputation bias.

---

## What's New in v1.0.1

- **Cryptographic shuffle**: `judge_pipeline.py` now uses `secrets.SystemRandom()` for truly random anonymization order — no positional bias possible
- **Holistic judge analysis**: Judge is instructed to write an "Overall Assessment" that identifies cross-model patterns, not just repeat per-result notes. `save_results.py` extracts this section separately for web display
- **Improved polling**: Poll every 20s (was 30s); always exit immediately when all agents done; minimum 3 polls before timeout
- **Progress reporting rules**: Explicit rules for what to send (status only) vs. never send (content) during polling
- **Web display**: Timestamps no longer shown as raw ISO strings; formatted date-only in table; full UTC datetime in expanded view
- **judge_analysis_full**: JSON results now store both the extracted holistic assessment (`judge_analysis`) and the complete judge output (`judge_analysis_full`)
- **Version bumped**: `update_modelshow_index.py` now writes `"version": "1.0.1"` to index

---

## Use Cases

### 🔍 Fact Checking
Ask a factual question and compare how models handle accuracy, sourcing, and hedging. Useful for spotting overconfident wrong answers, finding the most complete explanation, or verifying that multiple models agree on a key point.

**Example:** `mdls what caused the Bronze Age Collapse?`

### 🎨 Creative Tasks
See how different models interpret a creative brief. You'll get genuinely different tones, styles, and angles — great for inspiration, comparing narrative voice, or finding the approach that fits your project best.

**Example:** `mdls write a short poem about working late at night`

### ⚙️ Technical Decisions
Ask about architectural trade-offs, language choices, or system design patterns. Models often have different opinions, and seeing where they agree (or strongly disagree) is itself informative.

**Example:** `mdls pros and cons of event sourcing vs traditional CRUD`

### 👁️ Code Review
Submit a snippet and ask multiple models to review it. Different models notice different issues — one might catch a performance problem, another a security concern, another a readability issue.

**Example:** `mdls review this Python function for potential issues: [paste code]`

### 💡 Brainstorming
When you want a wide range of ideas rather than one "best" answer, multi-model output naturally produces more diverse suggestions. Compare approaches and cherry-pick from the best of each.

**Example:** `mdls give me 5 creative names for a productivity app for developers`

---

## Configuration (`config.json`)

| Key | Description |
|-----|-------------|
| `keyword` | Primary trigger: `mdls` |
| `models` | List of model aliases to query in parallel |
| `judgeModel` | Model used for double-blind judging |
| `timeoutSeconds` | Max wait time per model |
| `minSuccessful` | Minimum successful responses needed to proceed to judging |
| `blindJudging` | Whether to anonymize responses before judging (`true` by default) |
| `outputDir` | Where to save result files (default: `~/.openclaw/workspace/modelshow-results`) |
| `parallel` | Run models in parallel (`true`) or sequentially (`false`) |
| `showTopN` | Number of top results to display |
| `includeResponseText` | Include full response text in output |
| `blindJudgingLabels` | Label style for anonymization (`"alphabetic"`) |
| `shuffleBlindOrder` | Randomize response order before judging (`true`) |

---

## Scripts

### `judge_pipeline.py`
The core pipeline script. Two operations:

**Anonymize** (`action: "anonymize"`):
- Input: `{model_name: response_text}` dict
- Output: `anonymization_map`, `blind_responses_for_judge`
- Uses cryptographically secure randomization (`secrets.SystemRandom()`)

**Finalize** (`action: "finalize"`):
- Input: judge's raw evaluation text + `anonymization_map`
- Output: `deanonymized_judge_output`, `ranked_models_deanonymized`, `deanonymization_complete`

### `save_results.py`
Saves each run to `config.outputDir` in both Markdown and JSON. Resolves model aliases to full names and extracts the judge's "Overall Assessment" for the JSON output. The orchestrator runs this automatically after every comparison.

### `update_modelshow_index.py`
Optional utility to build a local index of result JSON files (e.g. for a custom dashboard or static site).

### `blind_judge_manager.py`
Utility module used by the pipeline for managing anonymization state.

---

## Quick Test

> The path below assumes a managed install (`~/.openclaw/skills/modelshow/`). If you installed via ClawHub into a workspace, substitute your actual skill path.

```bash
# Phase 1: Anonymize
echo '{"action":"anonymize","responses":{"sonnet":"Paris is the capital of France.","grok":"The capital of France is Paris, founded by the Parisii tribe."}}' | python3 ~/.openclaw/skills/modelshow/judge_pipeline.py

# Phase 2: Finalize (use anonymization_map from Phase 1)
echo '{
  "action": "finalize",
  "judge_output": "1st: Response A — Score: 8.5/10\nClear and direct.\n\n2nd: Response B — Score: 7/10\nMore detailed but slightly verbose.",
  "anonymization_map": {"Response A": "grok", "Response B": "sonnet"}
}' | python3 ~/.openclaw/skills/modelshow/judge_pipeline.py
```

Expected Phase 2 output:
```json
{
  "deanonymized_judge_output": "1st: **grok** — Score: 8.5/10\nClear and direct.\n\n2nd: **sonnet** — Score: 7/10\nMore detailed but slightly verbose.",
  "ranked_models_deanonymized": [
    {"placeholder": "Response A", "model": "grok", "score": 8.5, "rank": 1},
    {"placeholder": "Response B", "model": "sonnet", "score": 7.0, "rank": 2}
  ],
  "deanonymization_complete": true,
  "remaining_placeholders": []
}
```

---

## File Structure

```
modelshow/
├── SKILL.md              — Orchestrator workflow instructions
├── config.json           — Models, judge, timeout, keyword settings
├── judge_pipeline.py     — Anonymize + finalize pipeline (cryptographic shuffle)
├── save_results.py       — Saves results to MD + JSON in config.outputDir
├── update_modelshow_index.py — Optional: build local index / web index
├── blind_judge_manager.py — Anonymization utility
└── README.md             — This file
```