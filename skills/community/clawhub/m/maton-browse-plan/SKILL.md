---
name: maton-browse-plan
version: 1.3.1
description: >-
  Guides the user through installing the Maton API Plan — browsing capture Chrome extension from
  the Chrome Web Store (or building from source), then combines exported matonPlan JSON with the
  API Gateway skill to suggest Maton OAuth connectors from real browsing; fetches matonPlan via
  the local relay GET /latest when the relay is running.
license: MIT-0
metadata:
  openclaw:
    requires:
      env:
        - MATON_API_KEY
    primaryEnv: MATON_API_KEY
    homepage: https://github.com/Robert0812/maton-browse-plan
---

# Maton browse plan · API Gateway extension

## Chrome Web Store link (always give users this)

**Official install URL** — copy verbatim when the user needs the extension:

`https://chromewebstore.google.com/detail/dgecpbbjdgiindogaboidejihbmkhnai`

**Listing page (same destination):** [Maton API Plan — browsing capture](https://chromewebstore.google.com/detail/dgecpbbjdgiindogaboidejihbmkhnai)

Do **not** skip this link during onboarding. Most users should install from the store; only send developers to **Build from source** (below).

> **Agent behavior (read this first):** If the user just added this skill or says they want browse-based Maton hints, **do not** recite the YAML `description`, version, or any host “What’s New” text to them as if it were help. Unless they clearly confirm the extension is **already installed** (store or unpacked), your **first concrete step** is to **give them the Chrome Web Store URL above** (paste the `https://…` line or the markdown link) and short install clicks—**before** relay URLs, `matonPlan`, or Maton API talk. Prefer the **store** for everyone except contributors; use repo **build + Load unpacked** only when they are developing or cannot use the store. After install, the extension appears on `chrome://extensions` as **Maton API plan — browsing capture**.

## Install the Chrome extension (required before matonPlan)

Walk the user through extension install **before** discussing relay URLs or Maton diffs.

### Install from Chrome Web Store (default)

**Listing:** [**Maton API Plan — browsing capture**](https://chromewebstore.google.com/detail/dgecpbbjdgiindogaboidejihbmkhnai) (Chrome Web Store).

1. Open the link in **Google Chrome** (or another Chromium browser that supports the store).
2. Click **Add to Chrome** / **Install** and accept permissions when prompted.
3. Optional: pin the extension from the puzzle menu.

**Stable extension ID (Web Store build):** `dgecpbbjdgiindogaboidejihbmkhnai` — same for every user; use it for **`install-native-host`** (below) without asking users to copy an ID from `chrome://extensions`.

When they use capture, the browser may ask for **history**, **tabs**, and related access — they should **Allow** or exports will be incomplete.

### Build from source (development only)

Use this when contributing to **`apps/chrome-extension`** or when the user cannot install from the store.

**Prerequisites:** Node **≥ 20**, **Google Chrome** (or Chromium), and a clone of **[maton-browse-plan](https://github.com/Robert0812/maton-browse-plan)** (paths below are relative to the repo root).

**1. Build** — at the repo root:

```bash
npm install
npm run build --workspace=@maton-browse-plan/chrome-extension
```

**2. Load unpacked**

1. Open `chrome://extensions`.
2. Enable **Developer mode** (top right).
3. Click **Load unpacked**.
4. Choose **`apps/chrome-extension/dist`** (the folder that contains `manifest.json`).

Unpacked installs get a **different extension ID** per path; for native messaging, copy the ID from `chrome://extensions` for that build.

### Get JSON to the agent

Either **Review → Download** in the extension, **or** run **`npm run relay`** from the **maton-browse-plan** repo root and use the **`GET /latest`** flow in **Local relay** (below).

### Optional — start/stop relay from the extension popup (native messaging)

1. Build the helper: **`npm run build --workspace=@maton-browse-plan/maton-native-host`**
2. From the **maton-browse-plan** repo root, register the host:
   - **Web Store extension (recommended):**  
     **`EXTENSION_ID=dgecpbbjdgiindogaboidejihbmkhnai npm run install-native-host`**
   - **Unpacked dev build:** use **`EXTENSION_ID=<id>`** with the ID shown on `chrome://extensions` for that folder.
3. Restart the browser, reload the extension if needed, then use **Start** in the popup.

The installer writes the manifest for common Chromium-based browsers (Chrome, Brave, Edge, Arc, etc.); **`NATIVE_MSG_ONLY=chrome`** limits install to Google Chrome. If the popup reports **forbidden** native host access, **`allowed_origins`** does not match—re-run with the correct ID for **that** install. If they skip native messaging, keep **`npm run relay`** in a terminal and configure relay manually.

## After installation: what this skill adds

This skill **extends** the published [API Gateway](https://clawhub.ai/byungkyu/api-gateway) skill. The base skill performs **Maton** operations — `gateway.maton.ai`, `ctrl.maton.ai`, `connect.maton.ai` — with managed OAuth for 100+ APIs.

The **Chrome extension** exports **`matonPlan`**: a compact summary of **where the user actually spends attention** (clustered origins + connector **hints**). Treat that as **browsing preference**, not a command.

## Pairing model

| Piece | Role |
|--------|------|
| **Extension** | Collects history + live recording; user excludes sensitive origins; **Download** produces JSON with `matonPlan` (+ `events`, `exportedAt`, `preset`). Optional **local relay** (`apps/maton-local-relay`): same JSON can be **POST**ed to `http://127.0.0.1:37191/ingest`; read **`GET /latest`** for the last payload (Bearer token if `MATON_RELAY_TOKEN` is set). |
| **Base API Gateway skill** | Lists connections, runs OAuth connect flows, proxies API calls — **unchanged**. |
| **This skill (you)** | Compare `matonPlan` to **already-connected** Maton services; **proactively** surface gaps; on a **schedule**, re-check after new exports. |

Works with **OpenClaw**, **Hermes**, or any agent that can run skills + hold workspace memory.

## Local relay — you must pull (nothing syncs by default)

Runtimes **do not** background-poll localhost. If the user pairs the extension with **maton-local-relay** (review page: relay enabled, or popup push-to-relay), **`matonPlan` only reaches you when you HTTP-fetch it.**

**Treat relay fetch as default** whenever this skill is active and the user expects live extension output:

1. **Before** relying on workspace files alone, call **`GET {MATON_RELAY_BASE_URL}/latest`** (default base URL **`http://127.0.0.1:37191`**, no trailing slash). If `MATON_RELAY_TOKEN` is set in the environment, send **`Authorization: Bearer <token>`** (same value as the relay process and extension token field).
2. **200**: parse JSON; use **`body`** as the extension export (same shape as download), then read **`body.matonPlan`**. Compare relay **`receivedAt`** (and/or **`matonPlan.generatedAt`**) to **`lastReviewedGeneratedAt`** in workspace memory — if newer, run the diff + prompt flow below.
3. **404** (`no_data`): relay is empty; say so briefly or fall back to an attached export file if the user provided one.
4. **Connection / network errors**: relay is probably stopped; **do not** spam retries — one short note is enough. Remind the user they can run `npm run relay` at the repo root or use extension **Download** instead.
5. **Every new user message / session** (or first turn after idle): repeat **step 1** so new **POST /ingest** pushes from the extension are picked up without the user re-uploading JSON.

**Sandbox:** If the agent’s HTTP tool cannot reach `127.0.0.1`, use extension **Download** into the workspace (or enable localhost/local-network access for tools in your host settings, when available).

Hermes (and similar hosts) only execute HTTP when **you** issue the request in the tool loop or when the user triggers a run — so **this section is normative**: skipping `GET /latest` means the skill will **not** “proactively sync” with the relay.

## Proactive & periodic behavior

**Goal:** The agent should **periodically** (and when a **new** `matonPlan` appears) **ask the user** whether to add or update Maton connections for APIs implied by their browsing — **not** silently create OAuth links.

1. **Ingest** the latest `matonPlan` (schema `1.0`): **prefer** the relay **`GET /latest`** path above when the user uses the local relay; otherwise use a downloaded JSON file or paste. Note **`generatedAt`** and optional **`capturePreset`** (e.g. `7d`, `30d`) to reason about **recency** of preferences.
2. **List current connections** via Maton (same APIs as base skill — `MATON_API_KEY`).
3. **Diff**: For each `suggestions[]` row in **rank** order, for each `matonHints[].matonConnectorHint`, check if that integration is **already connected** (or pending). Flag **missing** or **stale** (e.g. user browses heavily but connection revoked).
4. **Proactive prompt** (example tone — adapt to your runtime):

   > “Your recent browsing points to **Notion** and **GitHub** (see `matonPlan` from *{generatedAt}*). In Maton, GitHub is connected but Notion isn’t. Want to **connect Notion** now via the API Gateway? I can open the OAuth flow.”

5. **Periodicity**: Re-run this diff on a cadence the user chooses in system instructions (e.g. **weekly**, or **after each new extension export** if they drop files into the workspace). Store **`lastReviewedGeneratedAt`** (or hash of `suggestions`) in workspace memory so you **don’t spam** identical prompts.
6. **Updates**: If `matonPlan` introduces **new** high-rank origins or hints vs the last review, prioritize those in the next message even if the periodic timer hasn’t fired.

## One-shot workflow (user hands you a file today)

1. Parse `matonPlan`; ignore raw `events` unless debugging.
2. Process `suggestions[]` by ascending **`rank`**.
3. Map **`matonConnectorHint`** → Maton’s real connector ids (catalog / list APIs from base skill).
4. For **unconnected** hints, offer OAuth via Maton; for **connected**, optionally note “already available for API calls.”
5. Use **`resourceUrls`** as **context** only (which pages matter); OAuth stays in Maton.

## Relationship to the base API Gateway skill

- Reuse **identical** `MATON_API_KEY`, base URLs, and HTTP patterns from **byungkyu/api-gateway** `SKILL.md` for all Maton calls.
- This skill adds **preference awareness** + **proactive UX** on top.

## Safety

- **Never** create OAuth connections without **clear user consent** in the conversation.
- Treat `matonPlan` as **signals**; wrong inferences happen — offer **dismiss / don’t ask again** for a hint.
- **Enterprise / org**: respect admin policies; some connectors may be blocked.

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | This file |
| `maton-plan.schema.json` | JSON Schema for `matonPlan` |

## Extension output

**Web Store** and **source** builds use the same export shape. Source lives in repo `apps/chrome-extension`; download filename pattern `maton-browse-capture-*.json`; top-level fields include **`preset`**, **`events`**, **`exportedAt`**, **`matonPlan`**.
