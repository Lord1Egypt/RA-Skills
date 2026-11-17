# paper-figure — submission-ready paper figures

**Figures are computed, not drawn.**

**Journal-compliant layout + a hard check + a fix list.** Turn "my figure was sent back" into one command: pipeline, architecture, mechanism and data figures laid out to the target journal's column width, type size, DPI and file format; a free local compliance check; and a cheap multi-model review that returns a list you can actually work through.

Local rendering and checking cost nothing, and **your paper data never leaves your machine**.

---

## The problem, in three sentences

1. A framework diagram stitched together in PowerPoint comes back with "figures do not meet our specifications": the journal wanted 89 mm, you sent 120 mm, the text is 4 pt and the export is 150 dpi.
2. Default matplotlib/Origin output is ugly, the legend collides with the curves, the red and green lines are indistinguishable to colour-blind readers, the axes have no units, and the EPS has no embedded fonts.
3. "AI generated my paper figure" is worse than ugly: the text is garbled, arrows point backwards, numbers are invented. That is a research-integrity problem, not an aesthetics problem.

> Retention signal, with its caveat: a comparable **free** academic-review skill on WorkBuddy saw 538 installs and 4,596 calls. That is usage of a free tool, **not paid conversion** — it only says these users come back to the same tool repeatedly.

## Before / after

| | Before (PowerPoint, defaults, one-click AI) | After (this tool) |
|---|---|---|
| Size | arbitrary, over column width, unreadable once shrunk | laid out at journal column widths (Nature 89/183 mm, Elsevier 90/190 mm, …), each rule with an official link and verification date |
| Type size | 4 pt, smaller after scaling | kept above journal minimums (Nature 5–7 pt, Elsevier 7 pt body, PLOS 8–12 pt) |
| Resolution | 72 dpi screenshots pasted in | vector first; raster exported at 300/600/1000 dpi at final size |
| Embedding & format | fonts missing from EPS, opens differently elsewhere | fonts embedded or outlined; format per journal (Nature main figures vector, PLOS TIFF/EPS) |
| Colour | red next to green, indistinguishable in greyscale | colour-blind-safe palette by default (Okabe–Ito, same family Nature publishes) |
| Text | overflows boxes, clipped at the canvas edge, two competing fonts | overflow estimation + one consistent font policy |
| Reproducible | one word changed, half the figure redrawn | edit one line of `figure.json`, re-run one command |
| AI images | garbled text, invented numbers, passed off as results | AI only for concept/cover/TOC, every output carries `*.ai-generated.json` |

Put plainly: **a figure that cannot be submitted has arrows crossing boxes, legends on top of curves and text you must zoom into; a figure that can has one arrow direction, in-figure legends and text that still reads at 89 mm.**

### Why not just ask an LLM for the matplotlib code

An LLM will give you code that runs, but not a figure that **meets the spec**. It does not know that Nature's single column is 89 mm or that a Nature figure is capped at 170 mm high, that Nature main figures accept vectors only, that the minimum type size is 5 pt — and it will not embed your fonts or check colour-blind safety for you. What we ship is a set of **templates checked line by line against the publishers' own author guidelines** (single/double column widths, minimum type size, font embedding, colour mode, 300/600/1000 dpi, panel a/b/c, colour-blind palettes, EPS/PDF/TIFF), where **every rule carries the official URL and its verification date** (`references/journal-specs.md`). That is the part an LLM cannot supply and cannot memorise.

### Trust boundary: exactly where AI fails

This is not "AI is not good enough" — it is that **we know where it always fails, so we keep it away from that step**:

| AI fails at | What it looks like |
|---|---|
| Text inside figures | `Sclentlst`, `Resuit`, Chinese turned into boxes or invented glyphs |
| Numbers | `0.85` rendered as `O.85`, axis ticks jumping 0, 3, 7, 12 |
| Arrow direction | A→B drawn as B→A, arrowheads on both ends, one reversed arrow among three |
| Data | looks like a bar or line chart, but the values are invented — retraction territory |

So the order is: **anything expressible deterministically (pipeline / architecture / mechanism / comparison / data) is drawn by code; only mood work (concept sketch / cover / TOC) goes to AI, labelled, with text and arrows added afterwards.** More examples in `references/prompt-library.md` and `references/failure-modes.md`.

**Cautionary case (sourced, secondary reporting).** On 2026-04-18 NEJM's *Images in Clinical Medicine* published a case photograph whose ruler scale, after AI processing, read `1, 3, ?, 4, ?, ?, ?, ?, 9`; the authors admitted using AI to reposition the ruler and not disclosing it as the journal requires, and the paper was retracted on 4-29 — 11 days after publication ([The Paper report](https://m.thepaper.cn/newsDetail_forward_33178035), collected 2026-11-03; NEJM's own notice and the PubPeer thread were not directly verified, so treat the detail as **unverified**). That is the hardest argument for "an AI image is never a data figure".

---

## Your data stays local

- `init` `spec` `chart` `render` `check` `export` **run entirely on your machine, offline**; your CSV, captions and unpublished results are **never uploaded**.
- Two things do use the network: `concept` sends an **English prompt**, and `review` sends **caption text plus the compliance summary** (optional — skip it and nothing is sent).
- Outputs live in `out/`. Add `out/` to `.gitignore` before submission so unpublished figures do not end up in a public repo.

---

## Install

Requires **Node >= 18** (built-in fetch is enough). No `npm install`, no Python, no Illustrator.

```bash
git clone https://github.com/u-claw-os/paper-figure.git
cd paper-figure
node scripts/fig.mjs wallet        # free: shows key source and balance
```

To use it inside an AI assistant (Claude Code, Codex, Cursor, DSH, …), drop the directory into your skills folder:

```bash
cp -r paper-figure ~/.dsh/skills/paper-figure
```

After that, "draw the pipeline figure for my paper, targeting a Nature sub-journal" triggers it.

---

## Four commands

```bash
# 1) create a workspace (brief.md / figure.json / data/ / out/)
node scripts/fig.mjs init ./fig1

# 2) turn plain-language brief.md into structured figure.json (local rules, no model, free)
node scripts/fig.mjs spec ./fig1

# 3) draw: structure/flow/mechanism/comparison via render; CSV data via chart
node scripts/fig.mjs render ./fig1 --journal nature
node scripts/fig.mjs chart  ./fig1

# 4) pre-submission check (free, every issue carries a fix), then export to journal specs
node scripts/fig.mjs check  ./fig1 --journal nature
node scripts/fig.mjs export ./fig1 --formats png,pdf --dpi 600
```

When `check` is green but you still want to know what an editor or reviewer would pick on:

```bash
node scripts/fig.mjs review  ./fig1 --tier econ   # multi-model review: fix list first, scores for comparison only
node scripts/fig.mjs concept ./fig1 --n 2         # concept/cover/TOC only, ~¥0.03 per image
```

The deliverable of `review` is a **fix list written as imperative actions** ("change the panel b legend from 4 pt to 7 pt"), not "8/10, decent". The three scores (visual 40 / information 40 / compliance 20) only compare two versions of the same figure; entries cut off by a model's token limit are flagged `truncated` and should not be trusted.

Every command writes JSON to stdout, human-readable progress to stderr, and on failure returns `{ok:false,error,fix}` with a non-zero exit code.

---

## Pricing

| Action | Cost |
|---|---|
| render / check / export / wallet | **free** (fully local) |
| AI concept image (`concept`) | ~**¥0.03** per image |
| Multi-model review (`review --tier econ`) | **¥0.01–0.07** per round |
| One figure, draft to submission-ready | ~**¥0.05–0.15** |

Roughly **¥1 covers ten figures end to end**. No Illustrator subscription, no Origin, no four foreign credit cards.

Price anchors (**official pages, November 2026**): [BioRender](https://www.biorender.com/pricing) — the free tier explicitly forbids publication use, individual plans from **$35/month**; [Origin store](https://store.originlab.com/) — OriginPro 2026b personal annual subscription **$310/year**; [Illustrator plans](https://www.adobe.com/products/illustrator/plans.html) — from **$22.99/month** (promotional tier; which tier maps to the single app versus the full suite is **unverified**).

The key is resolved automatically in this order: `--key` > `$XIAPAN_API_KEY` > `~/.dsh/aigc-wallet.json` > `~/.uking/device.json`. If none exists, bind a wallet (balance 0), then top up with Alipay:

```
https://u-claw.org.cn/recharge?key=<your-key>
```

The same wallet is shared by the rest of the tool family (model council, image/music generation, …).

---

## Trust boundary and research integrity

- **AI-generated images are limited to concept sketches, cover art, TOC graphics and talk/grant illustrations.**
- **An AI image must never be used as a data figure, results figure or statistics plot.** Generating a "bar chart" with an image model means inventing data — a retraction-grade problem.
- Every AI output is accompanied by `*.ai-generated.json` (model, prompt, timestamp, cost, suggested caption); declare AI involvement as your target journal requires.
- No fabricated data, no invented significance markers, no manipulation of experimental images.
- `check` reports "AI image used as a data figure" as an error and blocks it.
- Caption/figure agreement is judged by you and the reviewers in `review` — `check` only covers deterministic technical rules (size, type size, DPI, overflow, colour blindness, fonts), not natural-language caption content.

Before submitting, re-read the target journal's current Guide for Authors. Every entry in `references/journal-specs.md` carries a verification date; anything we could not confirm is marked **unverified (待核)** with a note on where to check — we do not publish numbers without a source.

---

## Who should not use this

- **You have no data but want a data figure anyway.** That is fabrication; there is no workaround here.
- **You need illustration-grade art or an icon library** (cells, equipment, molecules): use BioRender / Figdraw / Illustrator; we do not ship stock assets.
- **You want a drag-and-drop canvas**: use Figma / draw.io.
- **You want a guarantee of acceptance.** Journal specs change; we guarantee **traceable, fixable, sourced** — every rule has an official URL and a verification date that you can re-check before you submit.

---

## Troubleshooting

**`Invalid token` with a freshly copied key**
The balance is zero; the key is fine. Run `node scripts/fig.mjs wallet`, then top up ¥1.

**`No available channel`**
That model currently has no upstream channel on the gateway (image models more often than chat models). Use the default `gpt-image-2.5-1k`, or retry later — do not loop retries that spend money.

**Export cannot produce PNG**
Neither Chrome nor ImageMagick is installed. Deliver vector first (PDF/EPS/SVG — most journals accept them; Nature prefers PDF/EPS for main figures), then re-run `export` after installing Chrome.

**"Font size below journal minimum"**
The figure was drawn large and scaled down to column width, shrinking the text with it. Raise `font_size_pt` in `figure.json`, then `render` and `check` again.

**The review said a lot — which part do I trust?**
Trust `fixes`, not the scores; skip entries flagged `truncated: true`. Re-run the free `check` after each round of edits.

---

## Layout

```
scripts/            CLI plus render / check / export / AI bridge (zero dependencies)
references/         figure types, journal specs, prompt library, review checklist rules, failure modes
assets/             journals.json / palettes.json / journal.mplstyle
examples/           example workspaces you can edit directly
```

Read these three before drawing: `references/figure-types.md` (choosing the wrong figure type is the most expensive mistake), `references/journal-specs.md` (official links and verification dates — the core asset) and `references/failure-modes.md` (what a rejected figure looks like).

## Related tools (same wallet)

- [dsh-aigc](https://github.com/hfshfg/dsh-aigc) — image and music generation
- [dsh-panel](https://github.com/hfshfg/dsh-panel) — multi-model review panel
- model-consult — the same question answered by several models independently, then synthesised
- Top-ups: [u-claw.org.cn](https://u-claw.org.cn)

## License

MIT. Copyright (c) 2026 he fangsheng (hfshfg).
Figures you produce with this tool are yours (or your institution's) — we only wrote the layout code.
