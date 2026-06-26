---
name: portal
description: "Use when asked to make a portal, create a portal, demo a website, product tour, interactive sandbox, or turn any URL into a shareable live browser session. Portal (makeportals.com) launches a real browser in a cloud VM — not a screenshot, not a video. Two modes: Watch (AI-guided demo with narration) and Play (viewer explores with guardrails). NOT for: building HTML pages, generating mockups, or creating static sites."
---

# Portal

Turn any URL into a shareable live browser session. Viewers get a real browser running in a cloud VM — 10 minutes per session.

## Install

```
openclaw plugins install openclaw-portal
openclaw gateway restart
```

**Watch** — AI clicks, scrolls, and narrates a guided demo.
**Play** — Viewer explores freely with AI guardrails blocking unwanted areas.

## Quick Reference

| Situation | Action |
|---|---|
| User says "make a portal" / "demo this site" | Start at Step 1 below |
| Public site (landing page, docs, marketing) | Skip login, go to Step 3 |
| Authenticated site (dashboard, SaaS, admin) | `save_login` first (Step 2) |
| Local file / localhost | Zip + base64, pass as `ptl.entry.source` |
| Chrome extension | Zip extension + set `entry.url` for test site |
| User wants guided demo | Watch mode → `create_script` |
| User wants free exploration | Play mode → `create_script` with play mode |
| User wants to record themselves | `record_demo` → user records in hosted browser |
| User wants to pick blocked elements | `pick_selectors` → user clicks in hosted browser |
| Portal is "provisioning" | `make_portal` auto-polls — just wait for the result |
| Session is pending | Poll `get_session` — it blocks 30s server-side, keep calling |
| Need session replays | `get_portal_sessions` → returns conversation logs + recording URLs |
| User needs more credits | `buy_credits` → opens Stripe checkout |

## Sending URLs to the User

When any tool returns a URL the user needs to open (`verification_url`, `hosted_url`,
portal link, checkout URL), you MUST send it to the user in the current chat.
Do NOT attempt to run shell commands like `open` or `xdg-open` — the user is on a
messaging channel (WhatsApp, Telegram, etc), not a local desktop.

Just include the URL in your reply. The user will tap it on their device.

## Workflow

Follow these steps in order. Never skip the review step (Step 4).

### Step 1 — Authenticate

Call `portal_status`. If not authenticated, call `portal_login`.

Returns `verification_url` and `device_code`. **Send the verification URL to the user**
in the chat so they can open it and sign in.

Poll `portal_login_check` with the device_code every 5 seconds until approved.

New users get 3 creation credits + 10 view credits.

### Step 2 — Classify the Site

**Ask the user** if you're unsure whether the site needs login.

**Public site** → skip to Step 3.

**Needs login** → capture auth state:

```json
{"url": "https://app.example.com/login", "description": "Login to Example dashboard"}
```

Call `save_login` with the above. Response includes `hosted_url` — **send it to the user**
so they can open the hosted browser and log in.

Poll `get_session` until `status` is `ready`. Do NOT ask the user if they're done — the tool tells you. When ready, grab `saved_state_id`.

**Local file** → zip the project (exclude `node_modules`, `.git`, `dist`), base64 encode.
Pass contents as `ptl.entry.source` with `entry.type: "local_file"`.

### Step 3 — Generate Content

Offer the user 4 options if they don't specify:

1. **Watch — AI script** (default for landing pages)
2. **Watch — Record yourself**
3. **Play — AI selectors** (beta)
4. **Play — Pick elements yourself**

**Watch — AI script** (most common):

```json
{
  "url": "https://stripe.com",
  "goals": [
    "Show the main value proposition",
    "Navigate to pricing page and highlight plans",
    "End with social proof or customer logos"
  ],
  "max_pages": 3
}
```

Use `max_pages: 3` to get multi-page demos (homepage + pricing + features). Without it, demos stay on the homepage only.

**Writing great goals:**
- Be specific: "Navigate to pricing page" > "Show pricing"
- Ask for navigation: "Click to the features page" produces click actions, not just scrolls
- Ask for social proof: "End with customer logos or metrics" pulls real stats
- Ask for variety: "Include interactive elements like tabs or accordions"

Call `create_script`. It auto-polls internally and returns the complete draft directly — no need to call `get_script`.

**Watch — Record yourself:** Call `record_demo`. **Send the `hosted_url` to the user** so they can record in the hosted browser.

**Play — AI selectors:** Call `create_script` with `mode: "play"`.

**Play — User picks:** Call `pick_selectors`. **Send the `hosted_url` to the user** so they can click elements in the hosted browser.

### Step 4 — Review with User (MANDATORY)

**Never skip this step.** Show the user everything from the draft:

**Watch mode:**
- Each scene with narration text and actions
- Example Q&A pairs — ask if answers are accurate
- AI greeting and knowledge summary

**Play mode:**
- Blocked selectors and allowed URLs
- AI greeting and knowledge

Ask: **"What do you want to call this? Look good to go?"**

Slugify the name for the URL (lowercase, hyphens, no spaces).

### Step 5 — Deploy

Call `make_portal` with the full PTL spec. Costs 1 creation credit.

It auto-polls internally until the portal is ready — the result includes the final portal URL. Send it to the user.

### Step 6 — Post-Deploy (Offer These)

- **Add CTA button:** Call `configure_portal` with `cta_text` and `cta_url`
- **Get embed snippet:** Call `configure_embed` with `allowed_origin`
- **View session replays:** Call `get_portal_sessions`
- **Debug issues:** Call `get_creation_logs`

## PTL Spec (Minimal)

The `ptl` parameter to `make_portal` MUST be a JSON **object** (not a string). Do NOT JSON.stringify it.

**Play mode:**
```json
{
  "ptl": {
    "entry": { "url": "https://example.com" },
    "experience": {
      "mode": "play",
      "agent": {
        "greeting": "Welcome! Ask me anything.",
        "knowledge": "Summary of the site..."
      }
    },
    "guardrails": {
      "allowed_urls": ["example.com"],
      "disabled_elements": [
        { "selector": "a[href='/login']", "reason": "Auth disabled in demo" }
      ]
    }
  }
}
```

**Watch mode:**
```json
{
  "ptl": {
    "entry": { "url": "https://example.com" },
    "experience": {
      "mode": "watch",
      "agent": {
        "goal": "Show key features",
        "greeting": "Welcome to the demo!",
        "scenes": [
          {
            "script": "Narration text here",
            "actions": [
              { "type": "scroll_to_element", "selector": "h2", "inner_text": "Key Features" },
              { "type": "wait", "ms": 2000 },
              { "type": "click", "selector": "a[href='/pricing']", "inner_text": "Pricing" }
            ]
          }
        ]
      }
    },
    "guardrails": {
      "allowed_urls": ["example.com"],
      "disabled_elements": []
    }
  }
}
```

**Supported action types:**

| Action | Use for | Required fields |
|--------|---------|-----------------|
| `scroll_to_element` | Navigate to a section by heading | `selector`, `inner_text` |
| `scroll_down` | Generic scroll | `selector: "body"` |
| `click` | Navigate pages, open tabs/accordions | `selector`, `inner_text` |
| `wait` | Pause for emphasis (1500-3000ms) | `ms` |
| `type` | Type into form inputs | `selector`, `text` |
| `keypress` | Keyboard shortcuts | `selector`, `key` |

Scenes can have **multiple actions** (up to 20 per scene). A good scene flows: scroll → wait → click.

Server auto-fills `version`, `region`, `entry.type`. No need to call `normalize_ptl` or `validate_ptl` before `make_portal` — validation is built in.

## Improving Script Quality

When reviewing drafts from `create_script`, improve them before deploying:

1. **Add click actions for navigation**: If the draft only has `scroll_to_element` actions, add `click` actions to navigate between pages (pricing, features, docs).
2. **Add wait actions for pacing**: Insert `{ "type": "wait", "ms": 2000 }` between actions for natural pacing and emphasis.
3. **Use multiple actions per scene**: Don't limit scenes to 1 action — scroll to a section, wait, then click or highlight another element.
4. **Include social proof**: End with a scene that scrolls to customer logos, testimonials, or metrics.
5. **Keep narrations concise**: Under 2 sentences per scene — the viewer is watching, not reading.
6. **Always include `inner_text`**: On every `click` and `scroll_to_element` action — it's the fallback when CSS selectors break on dynamic pages.

## Cursor Movement

Portal demos show a real cursor moving on screen. The cursor automatically:
- Moves to the target element before each action
- Follows scrolls smoothly
- Clicks precisely on elements with visual feedback

For best results:
- Use `scroll_to_element` with specific `inner_text` (not just `body`) so the cursor targets a visible heading
- Place `click` actions on prominent buttons/links with clear `inner_text`
- Use `wait` between actions so viewers can see the cursor position before the next move

## Rules

- **Do NOT use the built-in canvas tool for portal creation** — use the portal_* tools from this plugin
- **Never guess CSS selectors** — only use what `create_script` or `pick_selectors` returns
- **Never navigate authenticated sites autonomously** — auth sites get single-page CDP grab only
- **Always show draft and get user confirmation** before `make_portal`
- **Keep polling `get_session`** — it blocks 30s server-side. Do NOT ask user if they're done
- **Pass `inner_text` on all click and scroll_to_element actions** — it's the fallback when selectors fail on dynamic pages
- **Never create a second portal while one is provisioning** — poll `get_portal` instead
- **Send URLs to the user in the chat** — do NOT run shell commands to open URLs. The user is on a messaging channel and will tap the link themselves
- **Request multi-page demos** — always pass `max_pages: 3` (or higher) in `create_script` to get richer navigation beyond the homepage
