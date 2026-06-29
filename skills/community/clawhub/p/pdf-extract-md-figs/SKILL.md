---
name: pdf-extract-md-figs
description: "Split a PDF (especially a scientific paper / 论文) into clean body-text Markdown PLUS a folder of extracted figure images that are saved but NOT read into context, so tokens are never wasted on irrelevant figures. Text goes through markitdown; figures are extracted with PyMuPDF, auto-separated into real numbered figures vs junk (logos/ads/TOC), indexed in a manifest mapping page→Figure number, and only opened one-at-a-time on explicit request. Use this skill WHENEVER the user uploads a PDF and wants to read/analyze/process/对比/梳理 it, OR says things like 'turn this paper into markdown', '把这篇PDF拆一下', '用这个skill', '提取图片但先别读图', 'process this PDF', or hands over a paper expecting figure-aware analysis. Trigger even if they only say '测试一下' / 'analyze this PDF' after uploading — default to this split-first, read-figures-on-demand workflow rather than dumping the whole PDF (with all its images) into context."
---

# PDF → Markdown + Figures (read figures on demand)

Turn a PDF into two cheap-to-read artifacts plus an on-disk figure library:

1. `<stem>.md` — body text via markitdown (headings flattened to plain text, tables/lists/citations preserved, equations and embedded figures lost — that's expected).
2. `<stem>_figs/` — every real figure saved as a PNG at native resolution, **never auto-read**.
   - Junk (logos, ads, TOC thumbnails) is shunted into `<stem>_figs/_misc/`.
   - Vector figures (no embedded raster) are auto-rendered as full-page PNGs.
3. `<stem>_figs/MANIFEST.txt` — a few-line index: page · file · size · **Figure number**.

## Core principle: never read a figure unless asked

The whole point is token economy. After running the script, read only the **Markdown** and the **MANIFEST** (both tiny). Do **not** `view` any PNG by default — figures are pixels and burn tokens. Open a figure only when the user names one ("看 Fig 3" / "read the calibration curve" / "what's in Figure 2?"), and open **only that one**, resolving its filename from the manifest. Reading every figure defeats the skill.

## Workflow

### 1. Run the splitter

```bash
pip install 'markitdown[all]' pymupdf --break-system-packages -q   # once
python3 scripts/pdf2md_figs.py "/path/to/paper.pdf" -o OUTDIR
```

The script prints the manifest to stdout. Options: `-o DIR` (output dir, default `<stem>_out/`), `--min-px N` (logo filter threshold, default 120 — lower it if a small legitimate figure gets dropped), `--dpi N` (resolution for vector-figure page rendering, default 200).

### 2. Read the cheap artifacts, report the index

Read `<stem>.md` for the body. Read `MANIFEST.txt` (or use the printed copy) and tell the user what figures exist, e.g. "Fig 1–5 extracted; 3 junk images (incl. an ad on p.12) isolated in `_misc/`." Proceed to analyze the **text** for whatever the user asked. Mention which figures hold data they might want, but don't open them yet.

### 3. Open figures only on explicit request

When the user names a figure, resolve it from the manifest (the **Figure** column maps page→number, so "Fig 3" → that row's filename), then `view` that single PNG and read off the data. If they ask for several, open them one by one, not all at once.

## What the manifest looks like

```
## 正文图(主文件夹)
  页  文件            尺寸(px)      Figure
  2  p02_img1.png    2045x2200    Fig 1
  5  p05_img1.png    1797x1601    Fig 3
## 疑似非正文图(_misc/ —— logo / 广告 / TOC,所在页无 Figure 图注)
  1  _misc/p01_img1.png   804x558
 12  _misc/p12_img1.png   1028x1382      ← e.g. a journal ad
```

A `p07_pagerender.png` entry with note "整页栅格化(矢量图)" means that page had a `Figure N` caption but no embedded raster, so the whole page was rendered — open it and crop visually if needed.

## How figures are classified (so you can trust the split)

Separation is by **caption presence**, not size: an image is a "real figure" only if its page contains a `Figure N.` / `Figure N:` caption. This is what keeps ads and TOC graphics (which sit on caption-less pages) out of the main folder — pure size filtering can't do that (an ad can be 1028×1382). If a real figure ever lands in `_misc/` (rare — e.g. a caption that says "Fig." not "Figure"), just open it from there; the files are all present either way.

## Known limits (state honestly, don't paper over)

- **Headings**: markitdown flattens `# / ##` to plain paragraphs (pdfminer has no layout model). The text is complete and readable; the hierarchy isn't marked.
- **Equations**: in-PDF equations come out garbled/split. For exact formulas, open the figure/page or the source.
- **Data inside figures** (calibration slopes, bar values): live in the images, absent from the Markdown — that's why they're extracted as PNGs to read on demand.
- **Header/footer cruft** (download watermarks, running heads) can leak into the Markdown; ignore or strip when summarizing.

## Dependencies

`markitdown[all]` (text), `pymupdf` (figures). Install once with the pip line above. The script is self-contained in `scripts/pdf2md_figs.py`.
