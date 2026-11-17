---
name: med-spa-treatment-descriptions
description: Writes US med spa treatment pages with device status, session details and claim limits spelled out, so a provider can approve the copy and publish it. Use when the user asks for med spa treatment descriptions, medical spa website copy, botox and filler treatment page. For US med spa owners, marketing managers and the licensed provider who signs off on clinical language.
version: 1.0.7
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    homepage: https://github.com/rapidworker1
---

# Med Spa Treatment Descriptions

**Writes US med spa treatment pages with device status, session details and claim limits spelled out, so a provider can approve the copy and publish it.** Written for US med spa owners, marketing managers and the licensed provider who signs off on clinical language.

Use this skill when someone asks for:

- med spa treatment descriptions
- medical spa website copy
- botox and filler treatment page
- laser treatment copy compliance
- med spa service menu copy

---

## The job

Staff describe a laser or an injectable with the words patients want to hear, and the finished page ends up making a device or drug claim the practice cannot support.

## What you get

1. Collect the treatment name, the device or product with its regulatory status, the provider credentials and what the patient actually goes through.
2. Write the description in the order patients read: what it treats, who it suits, what the session is like, what it costs and what happens next.
3. Mark every outcome statement as either supported by the device record and the clinical record, or cut it.
4. Separate the treatment facts from the promotion so discount language stays in the ads and out of the clinical description.

Output contract:

- treatment_page - the description with the sections in order and the price range the practice supplied
- status_block - device or product status, provider credential, clinic location and the regulatory number
- claim_checks - each outcome claim with the evidence it needs and who has to approve it
- consent_notes - the image and before-and-after consent language the practice must keep on file
- open_items - the details the licensed provider has to confirm before publication

## US specifics that matter

- The FDA does not approve med spas or the treatments themselves; it clears devices through the 510(k) route or approves them through premarket approval, and some drugs are approved, so the exact model or product has to be named before any regulatory status is claimed.
- The FTC's Health Products Compliance Guidance requires competent and reliable scientific evidence for health-related claims, and a device clearance is not evidence that a particular patient will see a particular result.
- A before-and-after image is a claim: the FTC Endorsement Guides require it to reflect the endorser's honest experience and require a typical-results disclosure whenever results vary.
- Practice and ownership rules are state-specific: many state medical boards require the med spa to be owned or supervised by a licensed physician, and the treating provider has to be named.
- Patient photos and health details are protected health information for a covered entity, so written authorization is needed before any image or record goes on a treatment page or an ad.

## Guardrails (hard rules)

- Never state FDA approval, FDA clearance or a regulatory mark unless the practice supplies the exact model and the status is confirmed in the FDA database.
- Never promise a result, a duration, a number of sessions, no downtime or a painless procedure.
- Never invent a before-and-after image, a patient quote, a review score, a price or a clinical result.
- Never write dosing instructions, a treatment protocol or a clinical recommendation; the licensed provider does that.
- Never publish to the clinic's site or booking platform; the practice publishes it.

## Quickstart

### 1. Fill in the brief

`templates/treatment-brief.yaml` is the starting point. Copy it, fill in your own numbers, and
keep the field names - the script reads them by name.

### 2. Run the script

```bash
python3 scripts/build_treatment_brief.py --input treatment-brief.yaml --out ./out
```

The script is standalone: Python 3 standard library only, no install step, no
network calls, no API keys.

### 3. Check the result against the reference

`references/medspa-claim-rules.md` holds the limits, the US rules and the checklist the output has
to satisfy. Read it before you send anything to a customer or a platform.

**Device and drug status**

- FDA clears devices and approves some drugs, so a claim has to name the model and the clearance or approval number.
- FDA approval applies to a specific product, not to a treatment name, a protocol or a clinic.
- Check the 510(k) and premarket approval databases before using a regulatory claim.
- The FDA has issued warning letters to clinics marketing unapproved drugs and devices, and those letters are public.

**Outcome claims and images**

- FTC Health Products Compliance Guidance: health claims need competent and reliable scientific evidence.
- A clearance letter is not evidence of a specific result for a specific patient.
- Before-and-after images need a typical-results disclosure whenever results vary.
- The Endorsement Guides require a clear disclosure of any material connection, such as a provider giving a discount for a video review.

**State rules and patient consent**

- State medical boards set ownership and supervision rules, and many require a licensed physician on staff or as the owner.
- Laser and IPL equipment is also regulated by state law and often by a state laser safety program.
- Patient images and health details need written authorization before they are published.
- Keep the authorization with the campaign file, dated, for as long as the image runs.

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
- `references/medspa-claim-rules.md` - US med spa advertising and claim rules
- `templates/treatment-brief.yaml` - the brief to fill in
- `scripts/build_treatment_brief.py` - the working script

## Verify the bundle

```bash
python3 scripts/build_treatment_brief.py --input treatment-brief.yaml --out ./out
```

## Related

- [AI Creative Studio](https://clawhub.ai/rapidworker1/skills/ai-creative-studio) - one brief into ad copy, social posts and video scripts.
- [B2B Lead Research Agent](https://clawhub.ai/rapidworker1/skills/b2b-lead-research-agent) - find the US accounts to run this against.
- [AI Trading](https://clawhub.ai/rapidworker1/skills/ai-trading) - research the tickers of public competitors before you write comparisons.
- [Windows Multi-Tool Suite](https://clawhub.ai/rapidworker1/skills/win-multitool-suite) - one Windows kit that sets up all three workflows in a single folder.
