# Marktplaats Seller Assistant - English Guide

## Name

**Marktplaats Seller Assistant**

Technical skill key: `marktplaats`.

The name is intentionally broader than search. The skill supports the selling workflow: category selection, live field inspection, photo preparation/upload, local ad tracking, repost preparation, dry-run review, and publishing only after explicit confirmation.

## Purpose

This skill helps an agent prepare, place, track and later repost Marktplaats advertisements safely and reliably. Its main value is that it inspects the current category-specific placement form before filling or submitting anything, then stores enough local metadata to revisit the ad later.

## Capabilities

- Search Marktplaats listings.
- Fetch category and subcategory information.
- Suggest the best category for an item.
- Inspect the live placement form in a logged-in browser session.
- Extract category-specific fields such as condition, brand, type, delivery, price and options.
- Prepare resized, metadata-reduced photo copies where possible.
- Upload photos through the logged-in browser context.
- Fill advertisement fields conservatively.
- Keep paid features disabled by default.
- Present a dry-run summary.
- Publish only after explicit approval for that exact advertisement.
- Report the success URL or validation errors after submission.
- Track posted advertisements locally.
- Mark expired or removed advertisements for reposting.
- Use photos and short item descriptions from WhatsApp/iMessage as ad intake when the user asks.
- Validate listing descriptions with the hard Copy Quality Gate before filling or publishing Marktplaats.

## What The Skill Must Not Do

- Do not publish or repost without explicit per-ad approval.
- Do not enable paid options without separate approval.
- Do not invent price, condition, or uncertain required fields.
- Do not bypass login, captcha, WAF, or security checks.
- Do not reply to buyers without separate permission.
- Do not expose cookies, XSRF tokens, or session data.

## Required Permissions

For search:

- Network access to Marktplaats.
- Node.js for the existing CLI tools.

For preparation:

- Read access to local photo files provided by the user.
- Read access to relevant WhatsApp/iMessage attachments when the user asks to use them.
- Write access for ad records, photos and snapshots, preferably:
  - `~/Documents/OpenClaw/Data/marktplaats/`
  - `housekeeping/marktplaats-snapshots/`
  - `housekeeping/marktplaats-test/`

For publishing:

- A browser session where the user is already logged in to Marktplaats.
- macOS automation through AppleScript or Peekaboo to use that browser context.
- Access to the Marktplaats placement page.

The skill does not need the user's Marktplaats password. Authentication stays inside the browser.

## Local Ad Register

Central register:

```text
~/Documents/OpenClaw/Data/marktplaats/advertenties.json
```

Optional per-ad directory:

```text
~/Documents/OpenClaw/Data/marktplaats/<slug>/
```

Recommended contents:

- `ad.json`: ad id, URL, status, price, category, source and repost metadata.
- `description.md`: latest listing description.
- `photos/originals/`: source photos.
- `photos/processed/`: resized/metadata-reduced publish photos.
- `snapshots/`: form or submit snapshots.

Important statuses:

- `draft`
- `pending_approval`
- `active`
- `removed`
- `expired`
- `needs_repost`
- `reposted`
- `test`

Update the register after every placement, validation error, removal, status check or repost.

## Reposting After Expiry

Marktplaats can change its rules. Check the current listing duration or ad status before relying on dates.

Standard flow:

1. Read `advertenties.json`.
2. Find active ads with past `renewAfter`/`expiresAt` values, or ads that no longer appear active.
3. Verify the ad status.
4. Set `needs_repost` when reposting makes sense.
5. Build a fresh dry-run from the existing text/photos, with current category and form checks.
6. Publish only after explicit user approval.
7. Add the new ad id to the register and keep the old ad in `repostHistory`.

A cron/heartbeat may report that ads need reposting, but it must not publish automatically.

## Intake From WhatsApp Or iMessage

When the user sends photos and says what the item is:

1. Read only the relevant messages/attachments.
2. Store photos in the ad directory.
3. Create safe publishing copies.
4. Record the source, such as channel, chat id, message id and timestamp.
5. Identify the item, brand/model and visible details.
6. Ask for missing essentials: price, condition, pickup/shipping, defects, missing parts.
7. Research product information online.
8. Choose a category and inspect the current form.
9. Write a strong SEO listing of roughly 3200-3500 characters.
10. Run `marktplaats-copy-qa` with product terms and a natural search variant.
11. Present a dry-run.
12. Publish only after explicit approval.

For WhatsApp/iMessage: reading/analyzing is allowed when the user asks for this task; sending replies to other people or buyers requires separate permission.

## Standard Workflow

### 1. Understand The Item

Determine:

- item type;
- brand/model/type;
- condition;
- asking price;
- pickup/shipping preference;
- included accessories;
- defects or important notes;
- available photos.

Ask the user if essential information is missing.

### 2. Find Candidate Categories

Use:

```bash
marktplaats-categories --json
marktplaats-categories <parent-id> --json
marktplaats-search "<product name>" --json -n 10
```

Choose based on:

- comparable listings;
- suitable category attributes;
- free listing availability;
- buyer discoverability.

Explain the chosen category in the dry-run.

### 3. Copy Quality Gate

Before filling Marktplaats, run:

```bash
marktplaats-copy-qa ./description.md \
  --require "<brand-or-type>" \
  --require "<product-kind>" \
  --variant "<natural search variant>" \
  --ad-json ./ad.json
```

Stop if the command fails or if `ad.json.copyQuality.passed` is not `true`.

Hard requirements:

- default length 3200-3500 characters;
- hard lower stop at 2800 characters;
- at least 7 substantial sections/paragraphs;
- no `Zoektermen:`, `Keywords:`, `SEO:` or keyword dump;
- natural SEO terms in prose;
- at least one subtle typo/spelling/search variant in context.

### 4. Inspect The Live Form

Open the placement page for the chosen category and capture a fresh snapshot with the probe:

```bash
node scripts/marktplaats-place-probe.js --browser --save housekeeping/marktplaats-snapshots/current.json
```

Inspect:

- `form.action` (usually `https://www.marktplaats.nl/plaats/ads`);
- category identifiers;
- presence of an XSRF token, not the value;
- hidden form values;
- title and description fields;
- price fields;
- condition fields;
- category attributes;
- delivery fields;
- postcode/contact fields;
- paid feature fields;
- selected bundle.

A `curl` probe on `/plaats` may return `401` without a session cookie. That is expected. In that case, use the logged-in browser DOM as the source of truth instead of manual UI clicking.

### 4. Fill Fields Conservatively

- Keep the title short and specific.
- Keep the description factual.
- Fill condition only when reasonably certain.
- Use the user's price or ask for one.
- Select multi-value attributes only when clearly applicable.
- Default delivery to pickup unless shipping is requested.

### 5. Enforce Free Listing

Before publishing, verify:

- free bundle selected;
- no urgent/homepage/promoted features enabled;
- no paid bundle selected;
- no payment page shown.

Stop if Marktplaats asks for payment unexpectedly.

### 6. Prepare Photos

Create temporary resized copies when possible:

```bash
mkdir -p housekeeping/marktplaats-test
sips -Z 1600 -s format jpeg input.jpg --out housekeeping/marktplaats-test/photo-1.jpg
```

Check for obvious EXIF/GPS metadata where possible.

### 7. Upload Photos

The proven browser-context upload uses:

- endpoint: `/plaats/api/image/upload`
- method: `POST`
- FormData fields:
  - `name`
  - `imageData`
- header:
  - `x-mp-xsrf`

Preferred local helper:

Upload the photos in the live flow and then read back the generated `images.ids` / hidden fields through the probe. Use the browser only as a session carrier, not to guess an upload path by hand.

### 8. Dry-Run Summary

Always show before publishing:

```text
Category: ...
Reason: ...
Title: ...
Price: ...
Condition: ...
Delivery: ...
Photos: ...
Free listing: yes/no
Paid options: none
Uncertain fields: ...
After approval: publish to Marktplaats
```

### 9. Publish

Publish only after explicit approval. After submission:

- report the success URL;
- report the advertisement id/link;
- summarize validation errors if any;
- stop if a payment page appears;
- update the local ad register.

## Testing Protocol

Recommended test period:

1. Start with one dummy/test advertisement.
2. Try 2-3 low-risk real ads.
3. Check category, price, photos and free options.
4. Confirm that ads can be removed easily.
5. Note problematic categories/fields.
6. Test reposting from the local register.
7. Test intake from WhatsApp/iMessage photos.
8. Consider ClawHub publication only after testing.

## ClawHub Publication Notes

A public listing should clearly state:

- publishing and reposting require explicit approval;
- the user must be logged in themselves;
- the skill does not bypass login/captcha/security checks;
- paid options are off by default;
- local ad tracking may contain personal photos/data and must be treated as private;
- required local tools and permissions;
- Marktplaats flows may change;
- users remain responsible for ad content and platform compliance.
