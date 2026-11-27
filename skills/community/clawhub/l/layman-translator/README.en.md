# layman-translator

[![skills.sh](https://skills.sh/b/shxuk/layman-translator)](https://skills.sh/shxuk/layman-translator)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/python-%3E%3D3.8-green.svg)](./scripts/style_check.py)

[简体中文](./README.md) | English

> **One-liner**: `layman-translator` is an open-source **Agent Skill + zero-dependency Python linting suite** for de-AI-ifying and humanizing Chinese technical writing through a 4-stage pipeline with strict fact-anchor alignment. Works completely offline.
> Best for **technical book authors, open-source documentation maintainers, and knowledge-base writers**; not intended for **cross-language translation or writing from scratch**.

---

## 30-Second Quick Start

```bash
# 1) Install as an Agent Skill (Claude Code / Cursor / Trae / Antigravity)
npx skills add shxuk/layman-translator

# 2) Run standalone Python checks locally (zero third-party dependencies)
python scripts/style_check.py path/to/draft.md
python scripts/fact_anchor_check.py path/to/01_orig.md path/to/02_edited.md
```

---

## What It Does (4-Stage Pipeline)

1. **Stage 0 · Format & Terminology**: Normalize punctuation, spacing, and technical terms without altering meaning (`format_check.py`).
2. **Stage 1 · De-AI Rewrite**: Strip translationese and AI clichés while making technical logic accessible to beginners.
3. **Stage 2 · Subtraction Only**: Remove meta-narration, fake colloquialisms, and redundant summaries without adding unverified claims.
4. **Stage 3 · Fact-Anchor & Style Audit**: Verify zero loss/hallucination of numbers, inline code, and proper nouns (`fact_anchor_check.py` + `style_check.py`).

## What It Does NOT Do

- Does not perform cross-language translation.
- Does not generate articles from scratch without a source draft.
- Immediately aborts if suspected real credentials (API keys, private keys, cookies) are detected in input.

## Project Facts

| Item | Value |
|---|---|
| Version | `1.0.0` |
| License | MIT |
| Runtime | Python ≥ 3.8 (stdlib only, 0 dependencies) |
| Scripts | `format_check.py`, `fact_anchor_check.py`, `style_check.py`, `consistency_check.py` |

## License

[MIT](./LICENSE)
