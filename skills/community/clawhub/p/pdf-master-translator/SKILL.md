---
name: pdf-master-translator
description: A highly robust, multi-agent pipeline for translating and reconstructing complex, image-heavy, or scanned PDF documents (especially engineering, scientific, or military specs). Use this skill when dealing with PDFs that contain complex layouts, dense tables, mathematical formulas (LaTeX), or when previous translation attempts resulted in broken layouts, missing figures, "hallucinated" translations, or corrupted text. It uses a "mask-and-fill" approach, holographic context injection, and SVG math rendering to ensure zero information loss and strict visual fidelity.
---

# PDF Master Translator (V10 Architecture)

This skill provides a battle-tested, "bulletproof" pipeline for translating complex PDF documents. It was forged from extensive trial and error on NASA engineering specifications. 

**Do NOT attempt to use simple OCR or zero-shot LLM translation for complex engineering documents.** They will fail. Use the `translator_engine_v10.py` script provided in this skill.

## Core Capabilities & The V10 Pipeline

This skill relies on a Python script (`scripts/translator_engine_v10.py`) that implements a specific, multi-agent workflow:

1. **Layout & Physical Isolation (Masking):** 
   - Never ask an LLM to "ignore the picture and translate the text" on a messy scan.
   - The pipeline first detects figures and tables. 
   - It **physically whites out (masks)** these regions on a temporary image.
   - The "clean" image is sent for translation, eliminating visual hallucinations.
   - Original figures are extracted, converted to Base64, and safely appended to the final HTML/PDF.

2. **Holographic Context Injection:**
   - Masking creates fragmented sentences around the masked areas.
   - To prevent the translation Agent from producing out-of-context or broken translations, the pipeline injects the **raw, unformatted text stream** of the entire page as a reference dictionary. The Agent uses this context to seamlessly bridge the visual gaps.

3. **Protocol Downgrade (XML over JSON):**
   - Forcing LLMs to output thousands of words of Markdown inside a strict JSON structure is fragile and prone to escaping errors.
   - The engine enforces simple XML tags (`<HEADER>`, `<BODY>`, `<FOOTER>`) for structural routing.

4. **Strict Math & Symbol Rendering:**
   - Standard PDF renderers (like WeasyPrint) cannot execute JavaScript (MathJax).
   - The script uses regex to intercept all LaTeX (`$...$` or `$$...$$`) and calls an external API (`math.vercel.app`) to render them as high-quality, embeddable SVG images.
   - The Prompt strictly mandates the format `**$Variable$**: Description` for symbol glossaries, ensuring visual consistency.

5. **Terminal Defense (Sanity Cleaner):**
   - The final step before PDF generation is a regex sweep to remove any leaked LLM artifacts (like ````markdown` wrappers) or error placeholders (like `RetryError[]`) that might have survived the pipeline.

## Usage Instructions

To use this skill, execute the `translator_engine_v10.py` script.

### Prerequisites

Ensure the required dependencies are installed (typically handled via `uv run` if inline metadata is used) and the Gemini API key is set.

```bash
export GEMINI_API_KEY="your_api_key_here"
# If a proxy is required for your network:
export HTTPS_PROXY="http://127.0.0.1:10809" 
```

### Execution

Run the script, providing the path to the target PDF and the specific page range.

```bash
uv run ~/.npm-global/lib/node_modules/openclaw/skills/pdf-master-translator/scripts/translator_engine_v10.py /path/to/target.pdf --start <start_page> --end <end_page>
```

**Important Operational Rules:**
- Always specify `--start` and `--end` explicitly.
- For very large documents (>20 pages), it is highly recommended to run this using `nohup ... &` in the background, as the multi-agent cross-checking and API rate-limiting sleep cycles make this a long-running process.

## Output

The script will generate a new PDF named `[OriginalName]_V10_FINAL_P[start]-[end].pdf` in the current working directory. 

This PDF will feature:
- A clear `--- Page X ---` divider for continuous reading.
- Consistent Header and Footer markdown tables.
- SVG-rendered math formulas.
- A dedicated `[ 原文图表/示意图 ]` section at the bottom of relevant pages containing the extracted original diagrams.
- (If applicable) A `[ 图例符号说明 ]` section containing translations of text found *inside* the diagrams.
