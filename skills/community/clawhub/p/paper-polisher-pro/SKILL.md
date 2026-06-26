# paper-polisher-pro — AI Detection & Academic Paper Polishing

> 🎯 **AI Detection · De-AI Rewriting · Paraphrase · Terminology Check · Quality Report**
> Bilingual (CN/EN) · 100% Local · Zero Upload · Zero Setup

## Why paper-polisher-pro?

Most AI detectors only catch ChatGPT. **This is the only open-source tool that fingerprints Chinese LLMs** — DeepSeek V4, GLM-5/5.1, Qwen 3.5/3.6, Kimi K2.5/K2.6, MiniMax M2.5, and Step — alongside GPT, Claude, and Gemini.

**Benchmark (2026 flagship models, long-form academic text):**
- Accuracy 98.0% · Precision 96.7% · Recall 100% · F1 98.3%
- 10 models tested: GLM-5, GLM-5.1, GLM-4.7, Kimi-K2.6, Kimi-K2.5, MiniMax-M2.5, DeepSeek-V3.2, DeepSeek-R1 — all 100% detection rate
- 0 false negatives on texts ≥100 characters

## Trigger Words

"polish paper", "deai", "reduce ai detection", "check ai writing", "paper polish", "rewrite paper", "humanize paper", "AI paper detector", "academic writing assistant", "AI writing checker", "remove AI traces", "humanize AI text", "thesis polishing", "dissertation polish", "detect AI writing", "AI writing score", "SCI paper editing", "manuscript polishing"

## Quick Start

### Detect AI Traces

```bash
python3 {{SKILL_DIR}}/scripts/ai_detector.py your_paper.txt --lang auto
```

Output:
```
📄 your_paper.txt
AI Risk Score: 68.5 / 100 🔴 HIGH
Paragraphs analyzed: 12
Top patterns: "it is worth noting" (×3), "plays a crucial role" (×2)
Suggestion: Rewrite paragraphs 2, 5, 8
```

### Check Terminology

```bash
python3 {{SKILL_DIR}}/scripts/term_check.py your_paper.txt
```

### Quality Report

```bash
python3 {{SKILL_DIR}}/scripts/quality_report.py your_paper.txt --format json
```

---

## AI Detection Engine (v1.1.0)

### 9-Layer Scoring System

| Layer | Weight | What it detects |
|-------|--------|-----------------|
| Pattern matching | 50 | 1,002 model-specific AI patterns (ZH 663 + EN 339) |
| Burstiness | 20 | 3-component variance analysis (human writing is uneven) |
| TTR (Type-Token Ratio) | 15 | Vocabulary diversity |
| Perplexity | 15 | Statistical predictability |
| Info density | 15 | Content density vs filler ratio |
| Sentence templates | 10 | Formulaic sentence structures |
| Opener patterns | 10 | Predictable paragraph starters |
| Length distribution | 5 | Unnatural uniformity |
| RLHF alignment | +bonus | Sycophantic/aligned phrasing |

### Supported AI Models (2026 Tested)

**Chinese LLMs (exclusive fingerprinting):**
DeepSeek V4 · V3.2 · R1 · GLM-5 · GLM-5.1 · GLM-4.7 · Qwen 3.5-397B · Qwen 3.6 · Kimi K2.5 · K2.6 · MiniMax M2.5 · Step

**International models:** ChatGPT · Claude · Gemini

### Pattern Library

| Language | Patterns | Categories |
|----------|----------|------------|
| Chinese | 663 | 18 categories (transition words, structural markers, medical templates, RLHF alignment, Kimi/DeepSeek/GLM fingerprints, etc.) |
| English | 339 | 9 categories (academic formal, filler phrases, markdown artifacts, RLHF alignment, etc.) |

Plus: 501 synonym groups, 25 Chinese sentence pattern templates.

---

## Full Workflow

### Step 1: AI Detection → Score + Pattern Breakdown

```bash
python3 {{SKILL_DIR}}/scripts/ai_detector.py <file> --lang auto --format json --output report.json
```

Returns 0–100 AI risk score, risk level, matched patterns per paragraph.

### Step 2: De-AI Rewriting (for paragraphs scoring ≥35)

**Chinese:** Remove filler ("值得注意的是", "综上所述"), break symmetrical structures, replace vague praise with data, vary sentence length, use content-based transitions.

**English:** Ban AI tells (plays a crucial role, has gained significant attention, delve into, myriad, plethora), use active voice, mix sentence lengths 5–30 words.

### Step 3: Smart Paraphrasing (5-layer)

1. Synonym replacement (501 groups, skip protected terms)
2. Voice transformation (active ↔ passive)
3. Word order shift
4. Abstraction ↔ expansion
5. Perspective shift

### Step 4: Terminology Standardization

2,255 authoritative terms (National Terms Commission + MeSH 2026 + Drug Terminology). Flags non-standard usage and suggests corrections.

### Step 5: Quality Report

Before/after comparison: AI score change, per-paragraph breakdown, terminology rate, readability metrics.

---

## Discipline Adaptation

- **Medicine/Biology**: Preserves clinical terms, drug names, dosages, statistics
- **Engineering/CS**: Protects algorithm names, formulas, performance metrics
- **Humanities/Social Sciences**: Allows opinionated phrasing, avoids AI summarization style
- **Business/Economics**: Preserves data and model names, replaces generic commentary

## Constraints

1. Never alter data — numbers, statistics, citations preserved exactly
2. 2,255 professional terms auto-protected during paraphrasing
3. Semantic fidelity — no information added or removed
4. Paragraph-by-paragraph processing for logical flow
5. All changes presented for user confirmation

---

## File Structure

```
paper-polisher/
├── SKILL.md                    ← This file (English, for ClawHub)
├── SKILL_ZH.md                 ← Chinese documentation (for SkillHub)
├── scripts/
│   ├── ai_detector.py          ← AI detection engine (v1.1.0, 9 layers, 1002 patterns)
│   ├── perplexity.py           ← Perplexity scoring module
│   ├── term_check.py           ← Terminology standardization (2,255 terms)
│   ├── ngram_similarity.py     ← N-gram repetition analysis
│   └── quality_report.py       ← Comprehensive quality report
├── references/
│   ├── ai_patterns_zh.json     ← Chinese AI patterns (663 rules, 18 categories)
│   ├── ai_patterns_en.json     ← English AI patterns (339 rules, 9 categories)
│   ├── synonyms_general.json   ← Synonym dictionary (501 groups)
│   └── sentence_patterns_zh.json ← Chinese sentence templates (25 patterns)
├── data/
│   └── terminology.json        ← Standard terminology database (2,255 terms)
└── templates/                  ← Prompt templates for rewriting
```

## Version History

- **v1.1.0** — Major upgrade: 9-layer detection engine (+perplexity, burstiness 3-component, sentence templates, RLHF alignment), pattern library expanded to 1,002 (ZH 663 + EN 339), synonym database 501 groups, benchmarked against 10× 2026 flagship models (98.3% F1 on long-form text)
- **v1.0.1** — English SKILL.md, SEO keywords
- **v1.0.0** — Initial release
