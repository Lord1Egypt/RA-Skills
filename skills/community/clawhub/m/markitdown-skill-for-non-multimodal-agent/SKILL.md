---
name: markitdown
description: "Use when a NON-multimodal agent (a text-only LLM backend that cannot read attachments) receives a document — PDF, Word (docx), PowerPoint (pptx), Excel (xlsx/xls), EPUB, HTML, CSV, JSON, XML, or ZIP — and you need its CONTENT to read, summarize, quote, or store it. The model can't open the file itself, so convert it to Markdown first with the markitdown MCP server (local, free, no API key). An OPTIONAL OCR layer reads scanned PDFs and images via an OpenAI-compatible vision model, but ONLY when a key is configured. Skip for files the agent can already read as plain text, and for plain images when no OCR key is set."
version: 0.1.0
homepage: https://github.com/Self-made-Orange/markitdown
metadata:
  openclaw:
    emoji: 📄
    requires:
      anyBins: [uvx, markitdown-mcp]
    envVars:
      - name: OPENAI_API_KEY
        required: false
        description: "OPTIONAL. Turns on the OCR layer (reading images and scanned PDFs) via the markitdown CLI. Costs API calls per image. Leave unset for free, text-only document conversion. Any OpenAI-compatible endpoint works — set OPENAI_BASE_URL to point elsewhere."
      - name: MARKITDOWN_OCR_MODEL
        required: false
        description: "Vision model used by the OCR layer. Default: gpt-4o-mini (cheapest vision-capable). Only read when OPENAI_API_KEY is set."
---

# markitdown — let a text-only agent read documents

A **non-multimodal** OpenClaw agent has no eyes: its backend is a plain-text API, so it cannot open a PDF / Word / Excel / PowerPoint attachment at all. This skill turns those files into Markdown the model *can* read.

Two layers, and you almost always only need the first:

- **Free layer — DEFAULT.** The `markitdown` MCP server converts text-bearing documents (PDF, docx, pptx, xlsx, html, csv, json, xml, epub, zip) to Markdown **locally**. No API key. No per-call cost. This handles the vast majority of attachments, because most documents store real text.
- **OCR layer — OPT-IN.** Scanned PDFs (photographed pages), standalone image files, and images embedded *inside* documents contain no extractable text — the only way to read them is to have a vision model look. This layer is **OFF unless `OPENAI_API_KEY` is set**, and it **bills per image**.

> The cost line is simple: pulling existing text out of a file is free; asking a model to *look at a picture* costs money.

## When to use

A document attachment arrives (Slack file, email attachment, a path the user gives you) whose extension or MIME is one of:

`pdf · docx · pptx · xlsx · xls · epub · html · htm · csv · json · xml · zip · md`
…and you need its **content** (to answer about it, summarize it, quote it, or save it).

For plain images (`png · jpg · jpeg · gif · webp · tiff`): only useful **if the OCR layer is on**. With no key, a text-only agent simply cannot read an image — say so rather than guessing.

Do **not** use this for a file the agent can already read as plain text in the prompt.

---

## Setup (operator, one time)

### Free layer — the MCP server

Run the server over stdio with no install using `uvx`:

```bash
uvx markitdown-mcp
```

Register it in your OpenClaw / MCP client config:

```json
{
  "mcpServers": {
    "markitdown": {
      "command": "uvx",
      "args": ["markitdown-mcp"]
    }
  }
}
```

This exposes one tool: **`convert_to_markdown(uri)`**, where `uri` is any `http:`, `https:`, `file:`, or `data:` URI. That is the whole free layer.

> The MCP server runs with the privileges of its process and can read any file that user can read. Keep it bound to local/stdio use only.

### OCR layer — the CLI (optional)

The MCP server **cannot OCR** — it never wires up a vision client, so even with plugins enabled it silently returns text-only output. OCR runs through the **CLI** instead. Install the fork (which ships the `markitdown-ocr` plugin) plus an OpenAI client:

```bash
pip install "git+https://github.com/Self-made-Orange/markitdown.git#subdirectory=packages/markitdown[all]"
pip install "git+https://github.com/Self-made-Orange/markitdown.git#subdirectory=packages/markitdown-ocr"
pip install openai
```

Then export a key (any OpenAI-compatible endpoint works):

```bash
export OPENAI_API_KEY=sk-...
export MARKITDOWN_OCR_MODEL=gpt-4o-mini   # cheapest vision model; optional
```

With no `OPENAI_API_KEY`, the plugin still loads but OCR is skipped — you fall back to the free converter automatically. So the OCR layer is genuinely zero-cost until someone opts in.

---

## Flow (per attachment)

1. **Get the absolute path.** The downloaded attachment's absolute path is already provided by the runtime (e.g. `MediaPaths`). Build a `file://<absolute-path>` URI.
   - ⚠️ Convert **in the same turn the file arrives** — downloads live in a temp dir and may be GC'd next turn.

2. **Free convert (always try first).** Call `convert_to_markdown("file://<abspath>")` on the `markitdown` MCP server. For normal documents you are done — read or store the Markdown.

3. **Decide if OCR is needed.** OCR only matters when:
   - the file is a **standalone image**, or
   - the free conversion came back **empty / whitespace-only / a few stray characters** (a tell-tale of a *scanned* PDF — pages are images, not text).

   If neither is true, stop. Don't spend a vision call on a document that already gave you text.

4. **OCR (only if needed AND `OPENAI_API_KEY` is set).** Shell out to the CLI:

   ```bash
   markitdown "<abspath>" --use-plugins --llm-client openai --llm-model "${MARKITDOWN_OCR_MODEL:-gpt-4o-mini}" -o "<out>.md"
   ```

   Or, with no global install, one-shot via `uvx`:

   ```bash
   uvx --from "git+https://github.com/Self-made-Orange/markitdown.git#subdirectory=packages/markitdown[all]" \
       --with "git+https://github.com/Self-made-Orange/markitdown.git#subdirectory=packages/markitdown-ocr" \
       --with openai \
       markitdown "<abspath>" --use-plugins --llm-client openai --llm-model "${MARKITDOWN_OCR_MODEL:-gpt-4o-mini}"
   ```

   OCR-extracted text is wrapped inline as `*[Image OCR] … [End OCR]*`, interleaved in reading order, so document structure is preserved.

   **If `OPENAI_API_KEY` is NOT set** and the content is image-only: do not pretend. Tell the user the file is image-based and reading it needs the optional OCR layer (an OpenAI-compatible key), and stop.

5. **Use or persist.** One-off question → read the Markdown and answer; no need to save. Worth keeping → write it to your knowledge store with provenance (original filename, source, date).

---

## Cost & model notes

- **Free layer:** $0. Local text extraction, no network model.
- **OCR layer:** one vision API call per image (and one per page for fully scanned PDFs, rendered at 300 DPI). With `gpt-4o-mini` this is roughly a fraction of a cent per image — cheap, but not zero, and it scales with image count. Pick a small vision model unless you need fidelity.
- The OCR layer is the reason this fork exists: it gives a text-only agent a way to "see" images, on demand, without making the whole agent multimodal.

## Gotchas

- **MCP ≠ OCR.** Do not set `MARKITDOWN_ENABLE_PLUGINS=true` on the server expecting OCR — the server passes no `llm_client`, so it silently skips OCR. OCR is CLI-only.
- **Path access.** Both the `file://` input and any output path must be inside the server/agent's allowed root, or the call is blocked.
- **Encrypted / corrupt files** can fail conversion. Report the failure plainly; for PDFs you can retry with a dedicated PDF tool if available.
- **Don't OCR what already has text.** Step 3's check exists to avoid burning vision calls on ordinary documents.

## Supported formats

Free (local): PDF, PowerPoint, Word, Excel, HTML, CSV, JSON, XML, EPUB, ZIP (iterates contents), plus text formats.
OCR-enhanced (key required): scanned PDFs, standalone images, and images embedded in PDF/DOCX/PPTX/XLSX.

---

Built on [microsoft/markitdown](https://github.com/microsoft/markitdown); OCR layer from the [Self-made-Orange/markitdown](https://github.com/Self-made-Orange/markitdown) fork (`packages/markitdown-ocr`).
