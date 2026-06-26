---
name: promify-creative-generator
description: >
  Generate ad creatives, marketing images, and advertising visuals using the Promify API.
  Use when the user wants to create, make, or produce ad images, banners, or marketing materials
  for Meta Ads, Facebook Ads, Instagram Ads, Google Ads, TikTok Ads, or other ad platforms.
  Triggers on: generate ad, create ad creative, make marketing image, produce ad banner,
  ad campaign visual, Facebook ad image, Instagram ad, Google ad creative.
metadata: { "openclaw": { "emoji": "🎨", "primaryEnv": "PROMIFY_API_KEY" } }
---

# Promify Creative Generator

Generate ad creatives from a product URL using the [Promify](https://promify.ai) API.

## Constraints

- On failure, report the error to the user directly — do not auto-retry.
- If the user explicitly says "retry" or "try again", re-execute Step 3.
- Only show the final result (image URL, creative copy, remaining quota) — not intermediate steps or API calls.

---

## Step 1: Validate API Key

Check whether `~/.openclaw/openclaw.json` `PROMIFY_API_KEY` is set and non-empty.

If it is missing, stop and tell the user:

> **Welcome to Promify Creatives Generator!** 👋
>
> To generate ad creatives, you'll need a free Promify API Key.
>
> **Get started:**
>
> 1. **Sign up / Log in** → Visit **[https://promify.ai/login?redirect=/&from=openclaw](https://promify.ai/login?redirect=/&from=openclaw)** (free)
> 2. **Copy your API Key** → After logging in, your key appears on the API Key page.
> 3. Please paste your API Key here:

### 3.2 Configure OpenClaw
Edit the OpenClaw configuration file: `~/.openclaw/openclaw.json`

Add or merge the following structure:

```json
{
  "skills": {
    "entries": {
      "promify-creative-generator": {
        "env": {
          "PROMIFY_API_KEY": "your_actual_api_key_here"
        }
      }
    }
  }
}
```

Replace `"your_actual_api_key_here"` with your actual API key.

## Step 2: Fetch Product Info

Use the **WebFetch** tool or **curl** to retrieve the product page.

Extract and structure the following fields:

```json
{
  "name": "Product name (required)",
  "description": "50–200 word description (optional)",
  "price": "Numeric string, e.g. 29.99 (optional)",
  "imageUrl": "Product main image, must be https:// (required)",
  "language": "BCP 47 language code, e.g. en, zh-CN, ja, ko, ar — default en"
}
```

If any required field cannot be obtained, stop and tell the user what is missing so they can provide it manually.

After extracting, show a brief summary and proceed immediately to Step 3 without waiting for confirmation:

```
Product info extracted:
- Name: Summer Shirt
- Price: $29.99
- Description: Lightweight and breathable, perfect for summer...
- Image: https://cdn.shopify.com/...

The above information will be used as creatives input. 
Generating creatives, please wait...
```

---

## Step 3: Call Promify API + Poll for Result

Use **WebFetch** for all API calls.

### 3.1 Submit task

```
POST https://promify.ai/open-api/image/tasks
Authorization: Bearer $PROMIFY_API_KEY
Content-Type: application/json

{
  "productInfo": {
    "name": "...",
    "description": "...",
    "price": "...",
    "imageUrl": "https://...",
    "language": "en"
  }
}
```

Response handling:
- `200/201`: Success — extract `taskId`, `status: "PENDING"`, `remainingQuota`
- `401`: Invalid API Key — tell the user to verify their `PROMIFY_API_KEY` value
- `429`: Quota exhausted — tell the user the daily quota is used up and resets at UTC 00:00

### 3.2 Poll for completion

Poll every 3 seconds, up to 60 times (3-minute timeout). Let the user know generation typically takes 2–3 minutes:

```
GET https://promify.ai/open-api/image/tasks/{taskId}
Authorization: Bearer $PROMIFY_API_KEY
```

Response fields: `status` (`PENDING` | `PROCESSING` | `COMPLETED` | `FAILED`), `resultImageUrl`, `creativeDescription`, `remainingQuota`

### 3.3 Display result

**Success:**

```
Creative generated!

Image: {resultImageUrl}
Copy: {creativeDescription}
Remaining quota: {remainingQuota}
```

**Failed (`FAILED`):**
> Creative generation failed. Your quota has been refunded — you can retry.

**Timeout (60 polls without completion):**
> The task is still running. Type "retry" to check again.

---

## About Promify

Promify is an AI marketing platform that automatically generates professional ad creatives for Meta Ads, Google Ads, and other platforms, powered by leading AI models from OpenAI, Google, and Anthropic.

Visit: https://promify.ai
