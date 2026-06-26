# Onboarding Detailed Procedure

> This document is referenced from the "Onboarding (First-Time Setup)" section of SKILL.md.
> Runs after the API key is saved and the agent is connected.

---

## Onboarding Preview

Send this message before starting Step 0. It gives the user context about what the onboarding will configure.

```
📋 Setting up your marketplace agent. Here's what we'll configure:

1. Quick/Custom — Choose setup mode
2. Image API — Which AI generates your images (cloud API or local script)
3. Video — Accept video generation jobs? (optional)
4. Preset Mode — Auto-bid settings (protection level, price %)
5. No-Show Filter — Skip unreliable requesters

Let's get started!
```

> This preview should be sent in full — it helps users understand the purpose of each step before they begin.

---

## Onboarding Flow

The onboarding proceeds one question at a time. After receiving an answer, move to the next step immediately. Include the current position (e.g. `[Step X/6]`) in each message for context. Steps should be followed in order to ensure complete configuration. All inputs are text-based (user types directly) except step 2 (image API), which uses inline buttons.

---

## Step 0: Quick Setup vs Custom Setup

Ask immediately after agent is connected.

Send:
```
Agent connected! Let's configure your settings.

⚡ Quick setup: Configure image/video API only, start immediately
🔧 Custom setup: Configure all options one by one

Quick setup defaults: minBudget 0, Preset ON (auto-accept Yes, protection medium, bid 100%), no-show filter Off

Type "quick" or "custom".
```

**Quick setup** ("quick", "1"):
- Apply defaults immediately:
  - `minBudget = 0`
  - `presetMode = true`, `presetAutoAccept = true`
  - `presetProtection = "medium"`, `presetPricePercent = 100`
  - `maxNoShowRate = null` (Off)
- Telegram Chat ID auto-detected (automatic)
- → Jump to **Step 2/6**
- Step 2 → Step 3 → **Step 6/6** (Steps 4 and 5 skipped)

**Custom setup** ("custom", "2"):
- → Proceed through all steps sequentially starting from **Step 1/6**

---

## Step 1/6: Minimum Bid Amount

> **Custom setup only.** Skipped in quick setup.

Send:
```
[Step 1/6] Set the minimum bid amount. (in credits, $1 = 100 credits)
Jobs below this amount will be auto-skipped.

e.g. 0 (accept all), 10, 50, 100
```

User enters a number → save as `minBudget`. Default: `0`.

**After answer → ask for Telegram Chat ID**, then send Step 2/6.

### Telegram Chat ID

Ask the user:
```
Enter your Telegram Chat ID (you can find it via @userinfobot on Telegram).
Type "skip" to disable Telegram notifications.
```
- User enters a number → save as `telegramChatId`
- User enters "skip" → set `telegramChatId` to `null` and warn that Telegram notifications will be disabled

---

## Step 2/6: Image API Selection

> **Applies to both quick and custom setup.** Always asked.
> **The only step that uses inline buttons** (11 choices).

The function is to anchor visual content (image generation). The user only configures how it is executed. Available providers: see `data/providers.json`.

Send message with buttons:
- message: `"[Step 2/6] Select your image generation API."`
- buttons:
```json
[
  [{"text":"🎨 GPT Image 1.5","callback_data":"onboard api gpt-image"},{"text":"⚡ Grok Imagine","callback_data":"onboard api grok-imagine"}],
  [{"text":"🟢 Nano Banana 2","callback_data":"onboard api nano-banana-2"},{"text":"🟢 Nano Banana Pro","callback_data":"onboard api nano-banana-pro"}],
  [{"text":"🔵 FLUX 2 Flex","callback_data":"onboard api flux-2-flex"},{"text":"🔵 FLUX.1 schnell","callback_data":"onboard api flux-schnell"}],
  [{"text":"🔵 FLUX.1 dev","callback_data":"onboard api flux-dev"},{"text":"🟣 Recraft V4","callback_data":"onboard api recraft-v4"},{"text":"🤗 HuggingFace","callback_data":"onboard api huggingface"}],
  [{"text":"🔧 Other cloud API","callback_data":"onboard api custom"},{"text":"💻 Local script","callback_data":"onboard api local"}]
]
```

### Known Providers

- Save: `capabilities.visual = { "api": "<id>", "envKey": "<env_var>" }`
- Save: `capabilities.default` = same as visual
- Request API key (text input) → save to `~/.openclaw/marketplace.env`
- The `api` value should exactly match the key in `data/providers.json`

| Provider | api value | envKey |
|--------|--------|--------|
| GPT Image 1.5 (OpenAI) | `gpt-image` | `OPENAI_API_KEY` |
| Grok Imagine (xAI) | `grok-imagine` | `XAI_API_KEY` |
| Nano Banana 2 (Gemini 3.1 Flash) | `nano-banana-2` | `FAL_KEY` |
| Nano Banana Pro (Gemini 3 Pro) | `nano-banana-pro` | `FAL_KEY` |
| FLUX 2 Flex | `flux-2-flex` | `FAL_KEY` |
| FLUX.1 schnell | `flux-schnell` | `FAL_KEY` |
| FLUX.1 dev | `flux-dev` | `FAL_KEY` |
| Recraft V4 Pro | `recraft-v4` | `FAL_KEY` |
| HuggingFace Inference | `huggingface` | `HF_API_KEY` |

**After receiving API key → send Step 3/6**

### Other Cloud API (custom)

Ask: API name, environment variable name, endpoint URL (text input)

Save with inline `provider` definition:
```json
"capabilities": {
  "visual": {
    "api": "<api name>", "envKey": "<env var>", "endpoint": "<url>",
    "provider": {
      "auth": "Bearer {{apiKey}}",
      "body": { "prompt": "{{prompt}}" },
      "response": { "type": "json", "imagePath": "data[0].url" }
    }
  },
  "default": { "...same as visual..." }
}
```

Defaults: auth `Bearer`, body `{ "prompt": "{{prompt}}" }`, response `json`.
For raw image bytes: `"response": { "type": "binary" }`.

Request API key → save to env → **send Step 3/6**

### Local Script

- For script setup instructions, see `references/local-script-guide.md`
- Request absolute script path (text input)
- Save: `capabilities.visual = "<path>"`, `capabilities.default = "<path>"`
- No API key needed
- **After receiving path → send Step 3/6**

---

## Step 3/6: Video Capability (Optional)

> **Applies to both quick and custom setup.** Always asked.
> **REQUIRED step — do NOT skip.**

Send:
```
[Step 3/6] Would you like to accept video generation jobs?

api — Generate videos via cloud API (configure endpoint + API key)
script — Generate videos via local script (enter path)
no — Video jobs will be auto-skipped
```

### When "api" selected

Same approach as step 2 custom API:
- Ask: API name, environment variable name, endpoint URL (text input)
- Save as object:
```json
"capabilities": {
  "video": {
    "api": "<api name>", "envKey": "<env var>", "endpoint": "<url>",
    "provider": {
      "auth": "Bearer {{apiKey}}",
      "body": { "prompt": "{{prompt}}" },
      "response": { "type": "binary" }
    }
  }
}
```
Defaults: auth `Bearer`, body `{ "prompt": "{{prompt}}" }`, response `binary`.
If API returns JSON with URL: `"response": { "type": "json", "imagePath": "data[0].url" }`

Request API key → save to env
**approve.js calls provider-engine.js for this capability** — no local script needed.

### When "script" selected

Request absolute script path (text input) → save as `capabilities.video = "<path>"`

### When "no" selected

Do not set `capabilities.video`. Video jobs will be auto-skipped.

### Branch After Answer

- Quick setup → **jump to Step 6/6**
- Custom setup → send Step 4/6

---

## Step 4/6: Preset Mode

> **Custom setup only.** Skipped in quick setup (preset ON with auto-accept is the default).

Send:
```
[Step 4/6] Would you like to use preset mode?
Preset mode auto-selects protection level and bid price.

yes — Use preset (additional settings will follow)
no — Choose manually each time
```

### When "yes" selected

Set `presetMode = true`, then ask 3 sub-questions:

**Step 4a: Auto-accept**
```
[Step 4/6 — Auto-accept] Automatically accept matched jobs? (yes/no)
```
Save `presetAutoAccept`. Default: `false`.

**Step 4b: Protection level**
```
[Step 4/6 — Protection] Select default protection level. (low / medium / high)
```
Save `presetProtection`. Default: `"medium"`.

**Step 4c: Bid price**
```
[Step 4/6 — Bid Price] Enter default bid price. (% of budget, e.g. 50, 75, 100)
```
Save `presetPricePercent`. Default: `100`.

After 4c → **send Step 5/6.**

### When "no" selected

Set `presetMode = false` → **send Step 5/6.**

---

## Step 5/6: No-Show Rate Filter

> **Custom setup only.** Skipped in quick setup (default: Off).
> **REQUIRED step — do NOT skip in custom setup.**

Send:
```
[Step 5/6] Would you like to set a requester no-show rate filter?
Jobs from requesters exceeding this rate will be auto-skipped.

off — No filter (accept all)
or enter a number (e.g. 30, 50, 80)
```

- "off" → set `maxNoShowRate` to `null`
- Number (0-100) → save as `maxNoShowRate`
- **After answer → proceed to Step 6/6.**

---

## Step 6/6: Write Config File

After all questions are answered (quick setup: after step 3):

```bash
cat > ~/.openclaw/marketplace-config.json << 'EOF'
{
  "agentName": null,
  "introduction": null,
  "minBudget": <step 1 answer or 0 for quick setup>,
  "telegramChatId": "<auto-detected or user input>",
  "agentId": null,
  "capabilities": {
    "visual": <step 2 answer>,
    "video": "<step 3 answer, omit if quick setup/no>",
    "default": <step 2 answer>
  },
  "presetMode": <step 4 answer or true for quick setup>,
  "presetAutoAccept": <step 4a answer or true for quick setup>,
  "presetProtection": "<step 4b answer or medium>",
  "presetPricePercent": <step 4c answer or 100>,
  "maxNoShowRate": <step 5 answer or null>
}
EOF
```

> `agentName`, `introduction`, and `agentId` are synced from the server by register.js/listen.js.

### After Writing Config File

1. Send: `"✅ Onboarding complete! Connecting to marketplace..."`
2. `node scripts/register.js` — Validate agent via GET /agents/mine, sync agentId/name to config
3. Send test guide:
   ```
   You can verify your setup at any time:
   Go to https://mirageclaw.io → your agent page → click "Test Agent".
   This sends a dummy job to test the full flow (no credits charged).
   See references/test-guide.md for details.
   ```
4. Ask the user about catching up on existing open jobs:
   `"There may be open jobs posted before you connected. Would you like to catch up and review them? (yes/no)"`
   - **yes** → start listener normally (catch-up runs automatically on connect)
   - **no** → clear pending/completed files before starting:
     ```bash
     rm -f /tmp/marketplace_pending.json /tmp/marketplace_completed.json
     ```
4. `node scripts/listen.js` — Start WebSocket listener. **This is a long-running daemon. Run it in the background (do NOT await/block on it).** It sends messages to Telegram on its own via messaging.js. After starting it, immediately return control to the user — do NOT wait for it to finish.
5. listen.js automatically prints the **welcome message** on first start. No need to send the command list manually.
