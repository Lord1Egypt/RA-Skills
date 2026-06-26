---
name: modelshow
version: 1.0.1
description: Blind multi-model comparison with architecturally guaranteed de-anonymization. Trigger with "mdls" or "modelshow" for double-blind evaluation of AI model responses.
metadata: {"openclaw": {"homepage": "https://github.com/schbz/modelshow", "emoji": "🕶️"}}
---

# ModelShow — Professional Multi-Model Evaluation

ModelShow provides a sophisticated framework for comparing AI model responses through double-blind evaluation. The system queries multiple models in parallel, anonymizes their outputs, and uses an independent judge model to rank responses purely on merit.

## Key Features

- **Architecturally Guaranteed De-anonymization**: The judge sub-agent automatically de-anonymizes results before returning them—orchestrators never see placeholder labels
- **Cryptographic Randomization**: Responses are presented to the judge in cryptographically secure random order using `secrets.SystemRandom()`
- **Holistic Judge Analysis**: Judges provide both per-model rankings and comprehensive "Overall Assessment" analyzing cross-model patterns
- **Intelligent Polling**: Automatic progress monitoring with content-free status updates and immediate completion detection
- **Professional Output**: Formatted results with scores, judge commentary, and actionable insights

## Detection

**Trigger**: Message starts with `mdls` or `modelshow` (case-insensitive). Extract the prompt by removing the trigger keyword.

**Example**: `mdls explain quantum entanglement` → prompt = `explain quantum entanglement`

## Workflow

```
Step 1  → Acknowledge & Load Configuration
Step 2  → Spawn Parallel Model Agents
Step 3  → Collect Responses with Intelligent Polling
Step 4  → Anonymize with Cryptographic Randomization
Step 5  → Spawn Judge+Deanon Sub-Agent
Step 6  → Parse De-anonymized Results
Step 7  → Build Formatted Output
Step 8  → Save Results (optionally update web index via update_modelshow_index.py)
```

### Step 1: Acknowledge & Load Configuration

**Immediate Response**:
```
🔄 ModelShow starting — querying models in parallel.
Results will appear automatically when judging is complete.
```

**Load Configuration**: Read `{baseDir}/config.json` for model list, judge model, timeouts, and other settings.

### Step 2: Spawn Parallel Model Agents

For each model in `config.models`:
- **Model**: The model alias (e.g., `pro`, `grok`, `kimi`)
- **Label**: `mdls-{model}-{timestamp}` (unique identifier)
- **Timeout**: `config.timeoutSeconds` (default: 360 seconds)
- **Task**: 
  ```
  {config.systemPrompt}
  
  {extracted user prompt}
  ```

**Parallel Execution**: If `config.parallel` is `true`, spawn all agents simultaneously.

**Context Handling**: If the prompt references external content (URLs, files, preferences), fetch and prepend this context to the task.

### Step 3: Collect Responses with Intelligent Polling

**Polling Strategy**:
- Poll every 20 seconds
- Exit immediately when all agents complete
- Minimum 3 polls before considering timeout
- Maximum runtime: `config.timeoutSeconds`

**Status Updates** (content-free):
- `⏳ Models responding... {done}/{total} complete. ({elapsed}s elapsed)`
- `✅ All {N} models responded. Sending to judge...`

**Response Collection**:
```python
collected_responses = {
  "model_name": {
    "status": "completed" | "failed" | "timeout",
    "text": "response text or empty string",
    "duration_seconds": duration
  }
}
```

**Minimum Success Check**: If successful responses < `config.minSuccessful`, abort with informative message.

### Step 4: Anonymize with Cryptographic Randomization

Execute the anonymization pipeline:
```bash
echo '{
  "action": "anonymize",
  "responses": {model: response_dict},
  "label_style": "alphabetic",
  "shuffle": true
}' | python3 {baseDir}/judge_pipeline.py
```

**Key Features**:
- `shuffle: true` ensures cryptographically random response order
- Labels are assigned as "Response A", "Response B", etc.
- `anonymization_map` tracks label-to-model mapping for later de-anonymization

### Step 5: Spawn Judge+Deanon Sub-Agent

The judge sub-agent performs both evaluation and de-anonymization in a single atomic operation:

**Judge Task Structure**:
```
You are an impartial judge AND a data processor.

Your task has TWO parts. Complete BOTH before returning anything.

═══════════════════════════════════════════════════════════
PART 1: JUDGE THE RESPONSES
═══════════════════════════════════════════════════════════

[Blind responses with placeholder labels]

═══════════════════════════════════════════════════════════
PART 2: PROCESS YOUR JUDGMENT
═══════════════════════════════════════════════════════════

1. Write your judgment evaluating Response A, Response B, etc.
2. Include scores (1-10) for each response
3. Provide an "Overall Assessment" section analyzing cross-model patterns

After writing your judgment, run this command:

echo '{
  "action": "finalize",
  "judge_output": "[YOUR JUDGMENT TEXT HERE]",
  "anonymization_map": {anonymization_map}
}' | python3 {baseDir}/judge_pipeline.py

Return ONLY the JSON output from that command.
```

**Judge Model**: Uses `config.judgeModel` (e.g. `sonnet`, `gemini31or`)

### Step 6: Parse De-anonymized Results

The judge sub-agent returns:
- `deanonymized_judge_output`: Full judgment with real model names
- `ranked_models_deanonymized`: Structured ranking data
- `deanonymization_complete`: Boolean verification

**Architectural Guarantee**: The orchestrator never receives placeholder labels—only de-anonymized results.

### Step 7: Build Formatted Output

Create professional presentation:
```
🕶️ Double-Blind Judging Results:

🏆 Model Name (Score: X.X/10)
[Full response text]
Judge's assessment: [Commentary]

🥈 Second Place (Score: X.X/10)
[Full response text]
Judge's assessment: [Commentary]

📊 Overall Assessment:
[Judge's holistic analysis of cross-model patterns]
```

> ⚠️ **WARNING: Step 8 is MANDATORY.**
> Sending results to the user is NOT the end of the task.
> You MUST execute Step 8 (save_results) immediately after sending.
> The task is NOT complete until `save_results.py` returns `{"success": true}`.
> Do NOT skip, defer, or omit Step 8 under any circumstances.

### Step 8: Save Results

> 🚨 **THIS STEP IS REQUIRED. DO NOT SKIP.**
> After every ModelShow run, you MUST save the results using `save_results.py`.
> Failure to save means the results are not persisted for later use.

**Save to `config.outputDir`** (default: `~/.openclaw/workspace/modelshow-results`):
- JSON: `{config.outputDir}/{slug}-{timestamp}.json`
- Markdown: `{config.outputDir}/{slug}-{timestamp}.md`

**Exact JSON payload to pipe into `save_results.py`:**

```json
{
  "prompt": "<the original user prompt>",
  "timestamp": "<ISO 8601 timestamp, e.g. 2026-03-08T01:00:00Z>",
  "models": ["model1", "model2", "model3"],
  "judge_model": "<config.judgeModel>",
  "output_dir": "<config.outputDir>",
  "ranked_results": [
    {
      "rank": 1,
      "model": "model_alias",
      "score": 9.5,
      "judge_notes": "Judge's per-model commentary here",
      "response_text": "The full model response text here"
    },
    {
      "rank": 2,
      "model": "model_alias",
      "score": 8.0,
      "judge_notes": "Judge's per-model commentary here",
      "response_text": "The full model response text here"
    }
  ],
  "deanonymized_judge_output": "<full judge output text with real model names>",
  "anonymization_map": {
    "Response A": "model_alias_1",
    "Response B": "model_alias_2"
  },
  "metadata": {
    "total_duration_ms": 45000,
    "successful_models": 4,
    "failed_models": 0,
    "timed_out_models": ["deepseek"]
  }
}
```

**Execute the save command:**
```bash
echo '<JSON payload above>' | python3 {baseDir}/save_results.py
```

**Verify success**: The script MUST return `{"success": true, ...}`. If it returns an error, fix and retry. Do NOT proceed without a successful save.

**Optional**: For building a local index of result files (e.g. for a custom dashboard or static site) or for web display (e.g. rexuvia.com), see `update_modelshow_index.py`. This is not part of the mandatory workflow.

> ✅ **Only after `save_results.py` returns success is the ModelShow task complete.**

## Configuration (`config.json`)

| Key | Description | Default |
|-----|-------------|---------|
| `keyword` | Primary trigger | `"mdls"` |
| `alternativeKeywords` | Also trigger on | `["modelshow"]` |
| `models` | List of model aliases to compare | `["pro", "sonnet", "deepseek", "gpt4", "grok", "kimi"]` |
| `judgeModel` | Model for double-blind evaluation | `"sonnet"` |
| `outputDir` | Where to save result files | `"~/.openclaw/workspace/modelshow-results"` |
| `timeoutSeconds` | Maximum wait time per model | `360` |
| `minSuccessful` | Minimum responses to proceed | `2` |
| `parallel` | Run models in parallel | `true` |
| `showTopN` | Number of top results to display | `10` |
| `includeResponseText` | Include full responses in output | `true` |
| `blindJudging` | Enable anonymization | `true` |
| `blindJudgingLabels` | Label style for anonymization | `"alphabetic"` |
| `shuffleBlindOrder` | Randomize response order | `true` |

## File Structure

```
modelshow/
├── SKILL.md              # This documentation
├── config.json           # Configuration settings
├── judge_pipeline.py     # Anonymization & de-anonymization pipeline
├── save_results.py       # Result saving with holistic assessment extraction
├── update_modelshow_index.py # Optional: build local index / web index
├── blind_judge_manager.py # Anonymization utility (legacy)
├── README.md             # User documentation
└── .gitignore            # Git exclusions
```

## Scripts

### `judge_pipeline.py`
Core pipeline for anonymization and de-anonymization:
- **`action: "anonymize"`**: Creates cryptographically randomized blind responses
- **`action: "finalize"`**: De-anonymizes judge output and extracts rankings

### `save_results.py`
Saves results in both JSON and Markdown formats with specialized extraction of the "Overall Assessment" section from judge output. Results are written to `config.outputDir` for local use, scripting, or your own tooling.

### `update_modelshow_index.py`
Optional utility to build a local index of result JSON files (e.g. for a custom dashboard or static site) or to update the web index for rexuvia.com. Not required for the core workflow.

## Usage Examples

**Basic Comparison**:
```
mdls explain the difference between TCP and UDP
```

**Creative Task**:
```
mdls write a short poem about working late at night
```

**Technical Analysis**:
```
mdls pros and cons of event sourcing vs traditional CRUD
```

**Code Review**:
```
mdls review this Python function for potential issues: [code]
```

## Best Practices

1. **Prompt Clarity**: Provide clear, specific prompts for meaningful comparisons
2. **Model Selection**: Choose models with complementary strengths for the task type
3. **Context Inclusion**: Reference relevant context when appropriate
4. **Result Interpretation**: Consider both scores and the judge's holistic assessment
5. **Tailor config**: Update `config.json` to match the models available on your instance
6. **Web Integration**: Optionally use `update_modelshow_index.py` to publish results

## Integration Points

- **Local storage**: Results are saved as JSON and Markdown in `config.outputDir` for local use, scripting, or your own tooling
- **Web display**: Use `update_modelshow_index.py` to make results available online
- **Cron Automation**: Can be scheduled for regular comparative analysis
- **API Access**: JSON results enable programmatic analysis

ModelShow represents state-of-the-art in AI model comparison, combining rigorous methodology with practical usability for both casual exploration and professional evaluation.
