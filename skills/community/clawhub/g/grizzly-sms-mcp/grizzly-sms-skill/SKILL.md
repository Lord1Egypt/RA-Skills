---
name: grizzly_sms
description: SMS verification and virtual phone numbers via Grizzly SMS API
metadata: {"openclaw":{"primaryEnv":"GRIZZLY_SMS_API_KEY","askForEnvInDialog":true}}
---

# Grizzly SMS Skill

Use this skill when the user needs: SMS verification, virtual numbers (Uber, Telegram, WhatsApp, Instagram, etc.), balance, prices, countries, services, or **account registration** with a rented phone number.

## API Key — Ask in Dialog

**Before running any Grizzly command**, you MUST ask the user for the API key (unless they already gave it in this conversation):

> Please provide your Grizzly SMS API key. Register on grizzlysms.com, then go to the API section (grizzlysms.com/docs) and copy the key.

**When the user provides the key in chat** — use it immediately. Pass it via exec env on every Grizzly call. Do NOT tell the user to set environment variables or edit config. The exec tool accepts env overrides; use them.

```
exec(command="node {baseDir}/scripts/grizzly-cli.mjs get_services", env={"GRIZZLY_SMS_API_KEY": "<exact_key_user_sent>"})
```

Example: user sends `e069d36075b9b230fe1eb159b86526d1` → use `env={"GRIZZLY_SMS_API_KEY": "e069d36075b9b230fe1eb159b86526d1"}` in exec. Then proceed with get_services, request_number, etc.

If the key is already in config (skills.entries.grizzly_sms.env), omit env. Otherwise always ask and pass via env.

**DO NOT** ask the user to set GRIZZLY_SMS_API_KEY in environment variables or config files when they already provided the key in chat. Use it directly.

## How to Call

There is NO tool named grizzly_sms.get_services(). You MUST use the **exec** tool. Example:

```
exec(command="node {baseDir}/scripts/grizzly-cli.mjs get_services", env={"GRIZZLY_SMS_API_KEY": "<user_key>"})
```

Use host=gateway only if tools.exec.host is configured for gateway. OpenClaw replaces {baseDir} with the skill folder path.

## Commands (run via exec)

| What to do | Exec command |
|------------|--------------|
| List services (find Uber) | `node {baseDir}/scripts/grizzly-cli.mjs get_services` |
| List countries (Brazil=73) | `node {baseDir}/scripts/grizzly-cli.mjs get_countries` |
| Check balance | `node {baseDir}/scripts/grizzly-cli.mjs get_balance` |
| Request number | `node {baseDir}/scripts/grizzly-cli.mjs request_number ub 73` |
| Get SMS code | `node {baseDir}/scripts/grizzly-cli.mjs get_status <activationId>` |
| Complete activation | `node {baseDir}/scripts/grizzly-cli.mjs set_status <activationId> 6` |

## Full Registration Workflow (any service, any country)

When the user asks to "register an account for [service] in [country]" (e.g. Uber in Brazil, Instagram in Jamaica):

1. **Ask for API key** (if not in config)
2. **Resolve service and country codes** — exec get_services and get_countries with env, parse JSON to find the code for the requested service (e.g. Uber → ub, Instagram → ig) and country (e.g. Brazil → 73, Jamaica → lookup in get_countries output)
3. **Request number** — exec request_number &lt;service&gt; &lt;countryId&gt; with env, save activationId and phone number
4. **Open browser and register** — use the **browser** tool to:
   - Navigate to the service registration URL (see table below)
   - Fill the phone number field with the rented number
   - Fill other required fields (email, name, etc.) — ask user if needed
   - Submit the form
5. **Poll for SMS** — exec get_status &lt;activationId&gt; with env until SMS code arrives
6. **Enter code in browser** — use browser tool to fill the verification code field and submit
7. **Complete activation** — exec set_status &lt;activationId&gt; 6 with env

## Registration URLs (for browser tool)

| Service | Registration URL |
|---------|------------------|
| Uber | https://riders.uber.com/ |
| Instagram | https://www.instagram.com/accounts/emailsignup/ |
| Telegram | https://web.telegram.org/ |
| WhatsApp | https://web.whatsapp.com/ |
| Facebook | https://www.facebook.com/reg/ |
| Google | https://accounts.google.com/signup |

Use browser.navigate, browser.fill, browser.click as needed. Set browser headless=false so the user can see the process on Mac.

## Output Formatting (for user messages)

When sending phone numbers, activation IDs, or SMS codes to the user, always format them for easy copying:

- **Phone number** — on its own line, clearly labeled
- **Activation ID (actId)** — on its own line, labeled
- **SMS code** — on its own line, labeled

**If the channel is Telegram** — wrap each value in monospace using triple backticks. Example:

```
Phone: `+15551234567`
Activation ID: `12345678`
SMS code: `847291`
```

Or as a compact block:
```
`+15551234567` | actId: `12345678` | SMS: `847291`
```

**If the channel is not Telegram** — use plain labeled format with clear line breaks. Avoid extra punctuation around the values so the user can select and copy easily.

## Service codes: tg, wa, ig, ub, fb, go
