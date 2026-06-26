---
name: humanize-ai-text
description: Remove signs of AI-generated writing from text. Detects AI vocabulary, puffery, and chatbot artifacts.
author: @biostartechnology
version: 1.0.0
license: MIT
metadata: {"clawdbot":{"emoji":"✍️","requires":{"bins":["python3"]}}}
---

# Humanize AI Text

Remove signs of AI-generated writing from text. Use when editing or reviewing text to make it sound more natural and human-written.

Based on Wikipedia's comprehensive "Signs of AI writing" guide.

## Features

- **AI Detection**: Identifies 16 pattern categories of AI-generated text
- **Pattern Categories**:
  - Citation bugs
  - Knowledge-cutoff phrases
  - Chatbot artifacts
  - Markdown/code remnants
  - AI-specific vocabulary
  - Filler phrases
  - Punctuation quirks
  - Stylistic parallelisms
  - Inflated symbolism
  - Promotional language
  - Superficial -ing analyses
  - Vague attributions
  - Em dash overuse
  - Rule of three
  - Negative parallelisms
  - Excessive conjunctive phrases

- **Diagnostic Reports**: Generate detailed AI detection reports
- **Text Transformation**: Rewrite text to sound more human
- **Comparison Mode**: Compare original vs humanized versions

## Usage

### Detect AI Writing

```bash
# Basic detection
python skills/humanize-ai-text/scripts/detect.py text.txt

# JSON output
python skills/humanize-ai-text/scripts/detect.py text.txt -j

# Score only
python skills/humanize-ai-text/scripts/detect.py text.txt -s

# Pipe text directly
echo "This text might be AI-generated" | python skills/humanize-ai-text/scripts/detect.py
```

### Transform Text

```bash
# Basic transformation
python skills/humanize-ai-text/scripts/transform.py text.txt

# Output to file
python skills/humanize-ai-text/scripts/transform.py text.txt -o clean.txt

# Aggressive mode (more changes)
python skills/humanize-ai-text/scripts/transform.py text.txt -a

# Quiet mode (no progress output)
python skills/humanize-ai-text/scripts/transform.py text.txt -q
```

### Compare Versions

```bash
# Compare original and transformed
python skills/humanize-ai-text/scripts/compare.py text.txt

# Compare and save result
python skills/humanize-ai-text/scripts/compare.py text.txt -o document_v2.txt
```

## Installation

The skill is already installed. To use it, ensure you have Python 3 installed.

### Dependencies

No external dependencies required - uses Python standard library.

## Pattern Detection

The detection script identifies these AI writing patterns:

### 1. Citation Bugs
- Fake or unverifiable sources
- "According to experts" without specifics
- Generic study references

### 2. Knowledge Cutoff
- "As of my last update"
- "I don't have real-time information"
- Date-stamped limitations

### 3. Chatbot Artifacts
- "I'd be happy to help"
- "Great question!"
- "Let me break this down"
- Excessive hedging

### 4. AI Vocabulary
- "delve into"
- "testament to"
- "in conclusion"
- "it's worth noting"
- "important to understand"

### 5. Filler Phrases
- Unnecessary introductions
- Redundant summaries
- Padding content

### 6. Stylistic Issues
- Rule of three overuse
- Negative parallelisms
- Em dash overuse
- Excessive conjunctive phrases

## Best Practices

1. **Detect First**: Run detection before transformation
2. **Review Changes**: Always review transformed text
3. **Use Compare**: Compare versions to understand changes
4. **Iterate**: May need multiple passes for best results
5. **Custom Patterns**: Edit `patterns.json` to add custom detections

## Customization

### Add Custom Patterns

Edit `skills/humanize-ai-text/scripts/patterns.json`:

```json
{
  "custom_patterns": {
    "my_pattern": {
      "regex": "pattern_here",
      "replacement": "replacement_text",
      "description": "What this pattern detects"
    }
  }
}
```

### Batch Processing

Process multiple files:

```bash
for f in *.md; do
  python skills/humanize-ai-text/scripts/detect.py "$f" -s
  python skills/humanize-ai-text/scripts/transform.py "$f" -a -o "${f%.md}_clean.md" -q
done
```

## Output Formats

### Detection Output

```
AI Detection Report
===================
File: text.txt
AI Probability: 73%

Patterns Detected:
- AI Vocabulary: 12 instances
- Filler Phrases: 8 instances
- Stylistic Parallelisms: 5 instances
...
```

### Transformation Output

```
Original: "I'd be happy to delve into this important topic."
Humanized: "Let's explore this topic."
```

## Security Notes

- ✅ No external network calls
- ✅ All processing done locally
- ✅ No credential access
- ✅ Safe file operations only
- ✅ No data exfiltration

## Integration

### With Writing Workflow

1. Write draft (AI-assisted or not)
2. Run detection to check AI score
3. Transform if score is high
4. Compare versions
5. Manual review and final edits

### With Content Pipeline

```bash
# In CI/CD or pre-commit hook
python skills/humanize-ai-text/scripts/detect.py content.md -s
# Fail if AI score > threshold
```

## Troubleshooting

### False Positives

Some legitimate writing may trigger patterns. Review manually.

### False Negatives

AI models evolve. Update patterns.json regularly.

### Encoding Issues

Ensure files are UTF-8 encoded:
```bash
python skills/humanize-ai-text/scripts/detect.py file.txt --encoding utf-8
```

## Examples

### Example 1: Blog Post

```bash
# Check AI score
python skills/humanize-ai-text/scripts/detect.py blog_post.md -s
# Output: AI Probability: 68%

# Transform
python skills/humanize-ai-text/scripts/transform.py blog_post.md -o blog_post_clean.md -a

# Compare
python skills/humanize-ai-text/scripts/compare.py blog_post.md -o blog_post_clean.md
```

### Example 2: Email

```bash
echo "I hope this email finds you well. I wanted to reach out regarding..." | \
  python skills/humanize-ai-text/scripts/detect.py
```

### Example 3: Academic Writing

```bash
# Detect AI patterns in paper
python skills/humanize-ai-text/scripts/detect.py paper.md -j > report.json

# Transform with conservative settings
python skills/humanize-ai-text/scripts/transform.py paper.md -o paper_clean.md
```

## Resources

- Wikipedia: "Signs of AI writing"
- Original research on AI text detection
- Community pattern contributions

---

*For more info, visit: https://clawhub.ai/biostartechnology/humanizer*
