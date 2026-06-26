# AI-Generated Text Detection

Determine whether text was written by an LLM (ChatGPT, Claude, Gemini, etc.) using the GPTZero API — the leading AI text detector with ~99% accuracy and per-sentence scoring.

## Getting an API Key

1. Create a free account at [gptzero.me](https://gptzero.me)
2. Go to the [Dashboard](https://gptzero.me/dashboard)
3. Navigate to the **API** section and generate a key
4. Set as environment variable:

```bash
export GPTZERO_API_KEY=your_key_here
```

### Pricing (as of March 2026)

| Plan | Words/month | Price |
|------|-------------|-------|
| **Free** | 10,000 | $0 |
| **Premium** | 300,000 | $12.99/mo (annual) |
| **Professional** | 500,000 | $24.99/mo (annual) |
| **API** | 300,000+ | from $45/mo |

Documentation: [gptzero.me/docs](https://gptzero.me/docs)

## Usage

```bash
# Direct text
python3 scripts/check_ai_text.py "The text to analyze goes here..."

# From file
python3 scripts/check_ai_text.py --file essay.txt

# From stdin
cat article.txt | python3 scripts/check_ai_text.py --stdin
```

## Response

```json
{
  "result": "ai_generated",
  "ai_probability": 0.92,
  "confidence": 0.93,
  "method": "gptzero",
  "details": {
    "completely_generated_prob": 0.92,
    "average_generated_prob": 0.88,
    "class_probabilities": {"ai": 0.92, "human": 0.06, "mixed": 0.02},
    "sentences": [
      {"text": "First sentence...", "ai_probability": 0.95, "perplexity": 12.3}
    ]
  }
}
```

## How GPTZero Works

GPTZero uses deep learning models (Model 4.3b, March 2026) trained to distinguish human from AI text by analyzing:

- **Perplexity** — how surprised a language model is by the text (low = AI-like)
- **Burstiness** — variation in sentence complexity (low = AI-like)
- **Learned stylistic patterns** — trained on millions of human and AI samples
- **Per-sentence scoring** — classifies each sentence individually

Supports detection of content from: GPT-4/5, Claude, Gemini, LLaMA, and other major LLMs.

## Verdicts

| Result | AI Probability | Meaning |
|--------|---------------|---------|
| `ai_generated` | ≥ 0.8 | Very likely written by AI |
| `mixed_or_uncertain` | 0.5 – 0.8 | May be AI-edited or mixed content |
| `likely_human` | < 0.5 | Likely human-written |

## Limitations

- **Short text** (< 50 words): All detectors struggle with minimal input
- **Paraphrased AI text**: Rephrasing reduces detection accuracy
- **Mixed content**: Human-edited AI text is harder to classify
- **Domain-specific**: Scientific, legal, formulaic text may trigger false positives
- **Non-English**: Optimized primarily for English text
- **No offline mode**: Requires internet connection and valid API key
