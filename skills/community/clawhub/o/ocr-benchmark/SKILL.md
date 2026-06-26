---
name: ocr-benchmark
version: 2.0.0
description: Multi-model OCR benchmark and comparison tool. Run OCR on images using Claude (Opus/Sonnet/Haiku via Bedrock), Gemini (Pro/Flash via Google AI Studio), and PaddleOCR (optional). Compare accuracy against human-verified ground truth with fuzzy line-level scoring, generate ranked terminal reports and PPT exports. Use when user wants to (1) benchmark OCR across models, (2) compare OCR accuracy/cost/speed, (3) test a new model on existing images, (4) generate OCR comparison reports, (5) evaluate OCR quality for Chinese/English product packaging or documents.
---

# OCR Benchmark v2.0.0

Multi-model OCR accuracy comparison with **fuzzy line-level scoring**, cost tracking, and PPT report generation.

## Setup

### 1. Install dependencies
```bash
cd ~/.openclaw/workspace/skills/ocr-benchmark/ocr-benchmark
pip install -r requirements.txt
```

### 2. Configure environment variables

Set the variables for the providers you want to use:

```bash
# Bedrock (Claude models) — uses your existing AWS credentials
export AWS_REGION=us-west-2          # or your preferred region

# Gemini (Google AI Studio)
export GOOGLE_API_KEY=your_key_here

# PaddleOCR — OPTIONAL, skip if not available
export PADDLEOCR_ENDPOINT=https://your-paddle-endpoint
export PADDLEOCR_TOKEN=your_token    # optional auth token
```

> **Note on PaddleOCR:** This provider requires an external API endpoint.
> If `PADDLEOCR_ENDPOINT` is not set, it is **automatically skipped** — no error.
> If you don't have a PaddleOCR endpoint, simply don't set the env var.

### 3. Prepare images

Place your images locally (`.jpg`, `.png`, `.webp`). There is no automatic image download — provide local file paths on the command line.

---

## Quick Start

### Run benchmark on images
```bash
python3 scripts/run_benchmark.py \
  --images img1.jpg img2.jpg img3.jpg \
  --output-dir ./results \
  --ground-truth ground_truth.json
```

### Skip models with missing credentials (no error, just skips)
```bash
python3 scripts/run_benchmark.py \
  --images img1.jpg \
  --auto-skip \
  --output-dir ./results
```

### Run only specific models
```bash
python3 scripts/run_benchmark.py \
  --images img1.jpg \
  --models opus sonnet gemini3pro \
  --output-dir ./results \
  --ground-truth ground_truth.json
```

### Score-only mode (re-score without re-running OCR)
```bash
python3 scripts/run_benchmark.py \
  --score-only \
  --output-dir ./results \
  --ground-truth ground_truth.json
```

### Generate PPT report from scored results
```bash
python3 scripts/make_report.py \
  --results-dir ./results \
  --images img1.jpg img2.jpg img3.jpg \
  --scores ./results/scores.json \
  --output report.pptx
```

---

## Workflow

1. **Prepare images** — collect your `.jpg` / `.png` files locally
2. **Run benchmark** — `run_benchmark.py` calls each model, saves `{image}.{model}.json`
3. **Create ground truth** — see `references/ground-truth-format.md` for format
4. **Score** — run with `--ground-truth` to produce `scores.json` and a terminal table
5. **Report** — `make_report.py` generates a shareable `.pptx`

---

## Environment Variables

| Variable | Provider | Required? | Description |
|----------|----------|-----------|-------------|
| `AWS_REGION` | Bedrock | Optional | Default: `us-west-2` |
| `GOOGLE_API_KEY` | Gemini | **Yes** | Google AI Studio API key |
| `PADDLEOCR_ENDPOINT` | PaddleOCR | Optional | Endpoint URL; **auto-skipped if unset** |
| `PADDLEOCR_TOKEN` | PaddleOCR | Optional | Auth token for PaddleOCR |

**Missing variables:** If a model's required env var is missing, it is automatically skipped with a warning. Use `--auto-skip` for completely silent skipping.

---

## Available Models

See `references/models.md` for full model IDs, pricing, and provider notes.

| Key | Label | Provider |
|-----|-------|----------|
| `opus` | Claude Opus 4.6 | Bedrock |
| `sonnet` | Claude Sonnet 4.6 | Bedrock |
| `haiku` | Claude Haiku 4.5 | Bedrock |
| `gemini3pro` | Gemini 3.1 Pro | Google AI Studio |
| `gemini3flash` | Gemini 3.1 Flash-Lite | Google AI Studio |
| `paddleocr` | PaddleOCR | External endpoint |

---

## Scoring Logic (v2)

Scoring uses **fuzzy line-level matching** with Levenshtein edit distance (pure Python stdlib, no extra dependencies).

For each ground truth line, the best-matching model output line is found and classified:

| Type | Condition | Score |
|------|-----------|-------|
| **EXACT** | Identical after normalization | 1.0 |
| **CLOSE** | Edit distance < 20% of length (punctuation/apostrophe diffs) | 0.8 |
| **PARTIAL** | Edit distance < 50% of length (real errors but mostly correct) | 0.5 |
| **MISS** | No matching line found | 0.0 |

Additionally, **EXTRA** lines are detected: model output lines that don't correspond to any ground truth line.

Normalization strips: whitespace, apostrophes/quotes (`'`, `'`, `` ` ``), common punctuation (`*`, `✓`, `，`, `、`, `：`, `（）`, `【】` etc.), then lowercases.

### Example terminal output
```
========================================================================
  OCR BENCHMARK RESULTS
========================================================================
  #    Model                        Score  Details
------------------------------------------------------------------------
  🥇   Gemini 3.1 Pro               98.7%  Image001: 99% | Image002: 98%
  🥈   Claude Opus 4.6              88.3%  Image001: 90% | Image002: 87%
  🥉   Claude Sonnet 4.6            85.1%  Image001: 86% | Image002: 84%
  4.   Gemini 3.1 Flash-Lite        82.0%  ...
========================================================================

  📄 Image001
  ──────────────────────────────────────────────────────────────────────
  ┌─ Claude Opus 4.6 (90.0%)
  │  ✅ EXACT   │ 小胡鸭
  │  🟡 CLOSE   │ GT: Sam's Coffee
  │             │ Got: Sams Coffee  [dist=2]
  │  🟠 PARTIAL │ GT: 浓郁香气
  │             │ Got: 浓都香气  [dist=1]
  │  ❌ MISS    │ GT: 净含量580克
  │  ⚠️  EXTRA lines (1):
  │     + "Product of China"
  └──────────────────────────────────────────────────────────────────────
```

---

## Output Files

Each OCR run produces `{image}.{model}.json`:
```json
{
  "text_extracted": ["line1", "line2", ...],
  "brand": "...",
  "product_name": "...",
  "net_weight": "...",
  "ingredients": ["..."],
  "other_fields": {},
  "model": "Claude Opus 4.6",
  "model_key": "opus",
  "latency_seconds": 23.5,
  "input_tokens": 800,
  "output_tokens": 500
}
```

Scoring produces `scores.json` with per-image, per-line, per-model results.

---

## Key Findings (2026-03, product packaging)

Human-verified ranking:
- **Gemini 3.1 Pro** (98.7%) — Best accuracy, ~$0.006/image
- **Claude Opus 4.6** (92.3%) — High accuracy; occasional missed details
- **Gemini 3.1 Flash** (89.7%) — Best speed/cost ratio, 9.7s
- **Claude Sonnet 4.6** (88.5%) — Stable structured output
- **PaddleOCR** (67.9%) — Free, character errors on packaging
- **Claude Haiku 4.5** (42.3%) — Poor Chinese OCR

**Lesson:** Never assume any model is ground truth. Human verification is essential.
