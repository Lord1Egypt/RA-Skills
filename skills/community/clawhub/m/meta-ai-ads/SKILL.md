---
name: meta-ads
description: >-
  Create and manage Meta (Facebook & Instagram) ad campaigns, lead forms,
  audiences, pixels, and product catalogs via the Plai API. Also connects
  Facebook/Instagram and Google Ads accounts via OAuth. Use when the user
  asks to connect an ad account, create, pause, update, or report on Facebook
  or Instagram ads, set up lead generation forms, build custom or lookalike
  audiences, manage product catalogs, upload media, or view campaign
  performance insights.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - PLAI_API_KEY
        - PLAI_USER_ID
      bins:
        - node
    primaryEnv: PLAI_API_KEY
    emoji: "📣"
    homepage: https://plai.io
    install:
      - kind: brew
        formula: node
        bins: [node]
---

# Meta Ads via Plai

Manage Meta (Facebook & Instagram) advertising through the [Plai](https://plai.io) API.

## Setup

Requires two environment variables:

- `PLAI_API_KEY` — your Plai API key (from your Plai account dashboard)
- `PLAI_USER_ID` — your Plai user ID

## How to Run

All operations are run via:

```bash
node scripts/plai-meta.js <command> [options]
```

Options are passed as `--key value` pairs. JSON array/object values must be
passed as quoted JSON strings, e.g. `--locations '[{"id":"2537","type":"city","countryCode":"AE"}]'`.

---

## Account Connection

**This must be done before any ad operation.** If an ad tool returns
`"User has no connected Facebook account"` or similar, generate a connection
link and share it with the user so they can complete the OAuth flow.

### Generate an account connection link

```bash
# Connect Facebook / Instagram Ads account
node scripts/plai-meta.js create-connection-link --platform FACEBOOK

# Connect Google Ads account
node scripts/plai-meta.js create-connection-link --platform GOOGLE

# With a custom redirect after connection
node scripts/plai-meta.js create-connection-link \
  --platform FACEBOOK \
  --redirectUri "https://yourapp.com/connected"
```

**Required:** `--platform` (`FACEBOOK` | `GOOGLE`)
**Optional:** `--redirectUri` — URL the user lands on after completing OAuth

Returns a `link` the user must open in their browser to connect their account.
Share this link directly; do not attempt to open it automatically.

---

## Campaign Management

### List all campaigns

```bash
node scripts/plai-meta.js list-campaigns
```

### Create a campaign

```bash
node scripts/plai-meta.js create-campaign \
  --campaignName "My Campaign" \
  --campaignType LEAD_GENERATION \
  --budget 50 \
  --url "https://example.com" \
  --locations '[{"id":"2537","type":"city","countryCode":"AE"}]' \
  --primaryText '[{"text":"Join us today!"}]' \
  --images '["https://example.com/image.jpg"]' \
  --leadsFormId "1234567890"
```

**Required params:** `campaignName`, `campaignType`, `budget`, `locations`

**Required by type:**
- `LEAD_GENERATION` → also requires `--leadsFormId`
- `CONVERSIONS` / `OUTCOME_SALES` → also requires `--pixelId` and `--conversionGoal`

**Optional params:** `--url`, `--primaryText`, `--headlines`, `--images`, `--videos`,
`--interests`, `--gender` (`"1"` male / `"2"` female), `--minAge`, `--maxAge`,
`--targetLocales`, `--audienceId`

**Notes:**
- `--images` takes a JSON array of URL strings — they are automatically transformed to `{url}` objects.
- `--minAge` and `--maxAge` must both be provided together.
- `callToAction` is always `LEARN_MORE` (set automatically).

`campaignType` values: `LEAD_GENERATION` | `LINK_CLICKS` | `CONVERSIONS` | `OUTCOME_SALES`

---

### Create a message engagement campaign

Drives conversations via messaging apps (Messenger, Instagram DM, WhatsApp).

```bash
node scripts/plai-meta.js create-message-engagement \
  --campaignName "Chat with Us" \
  --budget 50 \
  --url "https://example.com" \
  --locations '[{"id":"2537","type":"city","countryCode":"AE"}]' \
  --messagingApps '["MESSENGER","WHATSAPP"]' \
  --multipleCreatives '[{
    "url": "https://example.com",
    "primaryText": "Chat with us today!",
    "greetingText": "Hi {{user_first_name}}! How can we help you?",
    "conversations": [{"title": "Learn more about our products"},{"title": "Get a quote"}],
    "image": "https://example.com/image.jpg"
  }]'
```

**Required params:** `campaignName`, `budget`, `url`, `locations`, `messagingApps`, `multipleCreatives`

**`messagingApps`** — JSON array of: `MESSENGER` | `INSTAGRAM` | `WHATSAPP` — always ask the user; never default.

**`multipleCreatives`** — JSON array of 1–10 creative objects. Each creative:
- Required: `url`, `primaryText`, `greetingText`, `conversations` (array of `{title}` objects)
- Optional: `headlines`, `phoneNumber`, `image` (URL), `video` (`{video_id, thumbnail_url}`)

**Optional campaign params:** `--interests`, `--gender`, `--minAge`, `--maxAge`, `--targetLocales`, `--audienceId`

### Get campaign insights

```bash
node scripts/plai-meta.js get-insights \
  --campaignId "123456789" \
  --startDate "2024-01-01" \
  --endDate "2024-01-31"
```

### Update campaign status

```bash
node scripts/plai-meta.js update-status --campaignId "123456789" --status ACTIVE
node scripts/plai-meta.js update-status --campaignId "123456789" --status PAUSED
node scripts/plai-meta.js update-status --campaignId "123456789" --status DELETE
```

`status` values: `ACTIVE` | `PAUSED` | `DELETE`

### Update campaign budget

```bash
node scripts/plai-meta.js update-budget --campaignId "123456789" --amount 100
```

---

## Lead Forms

### Check Lead Ads Terms of Service

Always run this before creating a lead form. If TOS is not accepted, the user
must accept at https://www.facebook.com/ads/leadgen/tos first.

```bash
node scripts/plai-meta.js check-leadform-tos
```

### List existing lead forms

```bash
node scripts/plai-meta.js list-leadforms
```

### Create a lead form

Requires user to provide all values — never assume or fabricate them.

```bash
node scripts/plai-meta.js create-leadform \
  --leadsFormName "My Lead Form" \
  --privacyPolicyUrl "https://example.com/privacy" \
  --privacyPolicyName "Privacy Policy" \
  --website_url "https://example.com/thank-you" \
  --questionPageCustomHeadline "Tell us about yourself"
```

---

## Targeting

### Search targeting locations (always use before creating a campaign)

```bash
node scripts/plai-meta.js search-locations --query "Dubai"
node scripts/plai-meta.js search-locations --query "United States"
```

Returns `{id, type, countryCode}` objects. Pass these directly to `create-campaign --locations`.

### Search targeting interests

```bash
node scripts/plai-meta.js search-interests --query "fitness"
node scripts/plai-meta.js search-interests --query "real estate" \
  --specialAdCategories '["HOUSING"]' \
  --specialAdCountries '["US","GB"]'
```

`specialAdCategories` values: `HOUSING` | `FINANCIAL_PRODUCTS_SERVICES` | `EMPLOYMENT`

Returns `{id, name, type}` objects. Pass to `create-campaign --interests`.

### Get targeting locales (language targeting)

```bash
node scripts/plai-meta.js get-locales
```

Returns numeric locale IDs. Pass as `--targetLocales '[65,24]'` to `create-campaign`.

---

## Audiences

### List custom audiences

```bash
node scripts/plai-meta.js list-audiences
```

### Create page engagers audience

```bash
node scripts/plai-meta.js create-page-audience \
  --name "FB Page Engagers" \
  --type FACEBOOK

node scripts/plai-meta.js create-page-audience \
  --name "IG Engagers" \
  --type INSTAGRAM
```

### Create lead form audience

All fields are **required** — ask the user for each one explicitly.

```bash
node scripts/plai-meta.js create-leadform-audience \
  --name "Lead Form Openers" \
  --description "People who opened our summer campaign form" \
  --leadFormIds '["12345","67890"]' \
  --type open
```

`type` values: `open` | `close` | `submit`

### Create lookalike audience

```bash
node scripts/plai-meta.js create-lookalike \
  --sourceType AUDIENCE \
  --sourceId "120231334546180123" \
  --audienceName "Lookalike - US" \
  --countryCode US
```

`sourceType` options: `AUDIENCE` (requires `--sourceId`) | `PAGE` (no sourceId needed)

---

## Pixels & Conversions

### List pixels

```bash
node scripts/plai-meta.js list-pixels
```

### List custom conversions for a pixel

```bash
node scripts/plai-meta.js list-conversions \
  --pixelId "123456789" \
  --campaignType CONVERSIONS
```

`campaignType` options: `CONVERSIONS` | `OUTCOME_SALES`

---

## Media

### List ad account media

```bash
node scripts/plai-meta.js list-media --type IMAGE
node scripts/plai-meta.js list-media --type VIDEO
```

Returns `{video_id, thumbnail_url}` for videos. Use these in `create-campaign --videos`.

### List Facebook page media

```bash
node scripts/plai-meta.js list-fb-media --type IMAGE
```

### List Instagram page media

```bash
node scripts/plai-meta.js list-ig-media
```

### Upload a video

```bash
node scripts/plai-meta.js upload-video --videoUrl "https://example.com/video.mp4"
```

Returns a `videoId`. Then poll until ready:

```bash
node scripts/plai-meta.js get-video-info --videoId "123456789"
```

Poll until `status` is `READY`, then use `video_id` + `thumbnail_url` in `create-campaign --videos`.

---

## Product Catalogs

### List catalogs

```bash
node scripts/plai-meta.js list-catalogs
```

### Create a catalog

```bash
node scripts/plai-meta.js create-catalog --name "My Store Catalog"
```

### Create a product feed (imports products from a URL)

```bash
node scripts/plai-meta.js create-catalog-feed \
  --catalogId "123456" \
  --name "Daily Feed" \
  --fileUrl "https://example.com/products.csv" \
  --currencyCode USD \
  --timezone "America/New_York" \
  --interval DAILY
```

### Get catalog feed status

```bash
node scripts/plai-meta.js get-catalog-feed --catalogFeedId "123456"
```

### List products in a product set

```bash
node scripts/plai-meta.js list-catalog-products --productSetId "123456"
```

### Create a product set

```bash
node scripts/plai-meta.js create-product-set \
  --catalogId "123456" \
  --name "Summer Collection" \
  --productIds '["prod1","prod2","prod3"]'
```

---

## Workflow Guide

### Before creating any campaign

1. Run `create-connection-link --platform FACEBOOK` if the Meta account is not yet connected — share the returned link with the user.
2. Run `search-locations` to get valid location IDs — never guess IDs.
2. Optionally run `search-interests` for interest targeting.
3. For `LEAD_GENERATION`: run `check-leadform-tos`, then `list-leadforms` or `create-leadform`.
4. For `CONVERSIONS`/`OUTCOME_SALES`: run `list-pixels` then `list-conversions`.
5. Run `list-media` if using existing account media for creatives.

### Campaign type decision

| Goal | Command | `campaignType` |
|---|---|---|
| Collect leads via a form | `create-campaign` | `LEAD_GENERATION` |
| Drive traffic to a website | `create-campaign` | `LINK_CLICKS` |
| Optimize toward a pixel event | `create-campaign` | `CONVERSIONS` |
| Optimize toward purchases | `create-campaign` | `OUTCOME_SALES` |
| Drive messaging conversations | `create-message-engagement` | `OUTCOME_ENGAGEMENT` |

### After creating a campaign

Campaigns are created **paused** by default. Run:

```bash
node scripts/plai-meta.js update-status --campaignId "<id>" --status ACTIVE
```

when the user confirms they are ready to go live.

---

## Error Handling

| Error message | Cause | Fix |
|---|---|---|
| `Unauthorized` | Invalid `PLAI_API_KEY` | Check the key in your Plai dashboard |
| `User has no connected Facebook account` | Meta account not linked in Plai | Run `create-connection-link --platform FACEBOOK` and share the link with the user |
| `User has no connected Google account` | Google Ads account not linked | Run `create-connection-link --platform GOOGLE` and share the link with the user |
| TOS not accepted | Lead Ads TOS pending | User must accept at facebook.com/ads/leadgen/tos |
