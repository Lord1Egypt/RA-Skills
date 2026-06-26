---
name: mail-agent
version: 0.2.0
description: Set up AI-powered Gmail monitoring in OpenClaw. Watches inbox via Google Pub/Sub and pushes important emails to Telegram. Use when the user wants to install mail-agent, set up email notifications, configure Gmail monitoring, or troubleshoot why email alerts aren't arriving.
homepage: https://github.com/nanaco666/openclaw-mail-agent
metadata: {"clawdbot":{"emoji":"📬","requires":{"bins":["gog","gcloud"]},"install":[{"id":"gog","kind":"brew","formula":"steipete/tap/gogcli","bins":["gog"],"label":"Install gog (brew)"},{"id":"gcloud","kind":"brew","formula":"google-cloud-sdk","bins":["gcloud"],"label":"Install gcloud (brew)"}]}}
---

Sets up mail-agent — an AI Gmail monitor that runs inside OpenClaw and delivers important emails to your Telegram.

When invoked, walk the user through every step below in order. Check each prerequisite before proceeding. Do not skip steps.

---

## Step 1 — Check gog

```bash
gog auth list
```

If no accounts are listed, stop and tell the user to set up gog first:
```bash
gog auth credentials /path/to/client_secret.json
gog auth add you@gmail.com --services gmail
```

Note which Gmail account is being watched (`GOG_ACCOUNT` or the default).

---

## Step 2 — Check Google Cloud

```bash
gcloud auth application-default print-access-token 2>&1 | head -1
```

If this fails (not logged in):
```bash
gcloud auth application-default login
```

Check if a suitable GCP project exists:
```bash
gcloud projects list
```

If no project exists, create one:
```bash
gcloud projects create mail-agent-YOUR_NAME --name "Mail Agent"
gcloud config set project mail-agent-YOUR_NAME
```

If a project exists, set it:
```bash
gcloud config set project YOUR_PROJECT_ID
```

Note the project ID — needed for plugin config.

---

## Step 3 — Enable APIs

```bash
gcloud services enable gmail.googleapis.com pubsub.googleapis.com
```

---

## Step 4 — Create Pub/Sub topic and subscription

```bash
gcloud pubsub topics create mail-agent-inbox
gcloud pubsub subscriptions create mail-agent-inbox-sub --topic=mail-agent-inbox
```

Grant Gmail permission to publish to the topic:
```bash
gcloud pubsub topics add-iam-policy-binding mail-agent-inbox \
  --member="serviceAccount:gmail-api-push@system.gserviceaccount.com" \
  --role="roles/pubsub.publisher"
```

---

## Step 5 — Install the plugin

```bash
openclaw plugins install https://github.com/nanaco666/openclaw-mail-agent/archive/refs/tags/v0.2.1.tar.gz
```

---

## Step 6 — Configure

Set required values (replace placeholders):
```bash
openclaw plugins config mail-agent --set chatId=YOUR_TELEGRAM_CHAT_ID
openclaw plugins config mail-agent --set gcpProject=YOUR_GCP_PROJECT_ID
openclaw plugins config mail-agent --set pubsubSubscription=mail-agent-inbox-sub
```

Set LLM for email classification (recommended — skip to use pass-through):
```bash
openclaw plugins config mail-agent --set llmApiKey=sk-...
openclaw plugins config mail-agent --set llmModel=gpt-4o-mini
```

To find your Telegram chat ID: message @userinfobot on Telegram.

---

## Step 7 — Restart OpenClaw

```bash
openclaw gateway restart
```

Wait a few seconds, then check logs:
```bash
openclaw gateway logs | grep mail-agent
```

Expected output:
```
mail-agent: watch registered, historyId=...
mail-agent: watching inbox
```

If you see `watch registration failed`, re-check Step 3 and Step 4.

---

## Step 8 — Test

Send a test email to the watched Gmail account with urgent content, e.g.:

> Subject: Urgent: server is down
> Body: Production database crashed, users can't log in.

Wait up to 60 seconds. A notification should arrive in Telegram.

If nothing arrives after 2 minutes:
```bash
openclaw gateway logs | grep mail-agent
```

Common issues:
- `telegram runtime not available` → restart OpenClaw gateway
- `watch registration failed` → APIs not enabled or wrong project
- `subscription error` → subscription name mismatch, check Step 4
- No logs at all → plugin not loaded, check `openclaw plugins list`

---

## Reconfigure / update settings

```bash
openclaw plugins config mail-agent --set KEY=VALUE
openclaw gateway restart
```

## Uninstall

```bash
openclaw plugins uninstall mail-agent
openclaw gateway restart
```
