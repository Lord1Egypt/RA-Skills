# Enrollment & Setup Guide

Complete guide to setting up your IdentyClaw Passport for API access.

This guide is for both humans and automation agents. **OpenClaw Gateway operators** create NEAR accounts with the [openclaw-identyclaw-plugin](https://github.com/discernible-io/openclaw-identyclaw-plugin) (v1.5.0+ CLI or optional agent tool). **Hermes, IronClaw, NanoClaw, Cursor, and custom SDK clients** use `gennearaccount` (or equivalent host-side account generation) plus client-side API login. The purchase portal step is the human-operated checkout step in all paths.

**Runtime routing:** see [agent-frameworks.md](agent-frameworks.md) (MCP `doc:reference:agent-frameworks`) for per-framework install links and capability matrix.

## Table of Contents

- [Choose your path](#choose-your-path)
- [OpenClaw: Plugin + Skill Route](#openclaw-plugin--skill-route)
- [Manual enrollment (all other agents)](#manual-enrollment-all-other-agents)
- [Prerequisites](#prerequisites)
- [Step 1: Create NEAR Account](#step-1-create-near-account)
- [Step 2: Purchase IdentyClaw Passport](#step-2-purchase-identityclaw-passport)
- [Step 3: Authenticate with Your NEAR Account](#step-3-authenticate-with-your-near-account)
- [Troubleshooting](#troubleshooting)

## Choose your path

| Audience | Route |
|----------|-------|
| **OpenClaw Gateway operators** | [OpenClaw plugin + skill route](#openclaw-plugin--skill-route) — plugin generates NEAR credentials (no `gennearaccount` binary), handles JWT login and API tools after Passport purchase |
| **Hermes Agent** | [hermes-integration-guide.md](hermes-integration-guide.md) — copy `hermes-identyclaw-skill/` to `~/.hermes/skills/` + manual enrollment below |
| **IronClaw** | [ironclaw-integration-guide.md](ironclaw-integration-guide.md) — MCP docs + `gennearaccount` + host sidecar for login/HOLA |
| **NanoClaw** | [nanoclaw-integration-guide.md](nanoclaw-integration-guide.md) — bind-mounted secrets + MCP/curl in container |
| **Cursor / Claude Desktop / custom SDK / shell** | [Manual enrollment](#manual-enrollment-all-other-agents) — `gennearaccount`, curl login, MCP `doc:skills` |

Both paths share the same on-chain prerequisites: a NEAR implicit account and a minted IdentyClaw Passport. **Account creation** and **post-purchase API integration** differ by path (OpenClaw plugin vs `gennearaccount` + client-side HTTP).

## OpenClaw: Plugin + Skill Route

**For OpenClaw users only.** Other AI agents must follow [manual enrollment](#manual-enrollment-all-other-agents) below.

The OpenClaw route uses the **openclaw-identyclaw-plugin** (v1.5.0+) for NEAR implicit account generation and post-purchase API integration, plus a **ClawHub skill** for workflow guidance. Passport purchase remains a human checkout step.

### What still requires manual steps

1. **Fund the NEAR account** — transfer NEAR for checkout and transaction fees
2. **Purchase Passport** — human checkout at https://purchase.identyclaw.com (see [Step 2](#step-2-purchase-identityclaw-passport))

There is no IdentyClaw MCP tool or plugin that replaces the purchase portal for minting. Non-OpenClaw agents must still use `gennearaccount` for account creation (see [Manual enrollment](#manual-enrollment-all-other-agents)).

### What the plugin + skill replace

- **`gennearaccount` on OpenClaw** — plugin operator CLI or optional `identyclaw_generate_near_account` tool writes gennearaccount-compatible JSON to `secrets/near-credentials/` (private key never returned to chat)
- Hand-rolled `GET /api/login/timestamp` → sign → `POST /api/login` (plugin caches JWT, applies `New-Token` headers, re-logins before expiry)
- Manual curl for identity, HOLA verify/create, agent discovery, and MCP doc fetch (plugin tools)
- Scattered protocol docs during daily operation (skill auto-triggers on identity/HOLA/DID prompts; `identyclaw_list_resources` / `doc:discovery` for deep references)

### 1. Install skill and plugin

```bash
openclaw skills install clawhub:identyclaw
openclaw plugins install clawhub:@identyclaw/openclaw-identyclaw-plugin
```

| Artifact | ClawHub | Role |
|----------|---------|------|
| Skill | [identyclaw/identyclaw](https://clawhub.ai/identyclaw/identyclaw) | When to use IdentyClaw, HOLA verify/create patterns, discovery guardrails |
| Plugin | [@identyclaw/openclaw-identyclaw-plugin](https://clawhub.ai/plugins/@identyclaw/openclaw-identyclaw-plugin) | NEAR account generation, JWT login, HOLA, identity, discovery (`identyclaw_generate_near_account`, `identyclaw_get_my_identity`, …) |

After `npm run prepare:publish` in a local checkout, install the plugin from path instead: `openclaw plugins install /path/to/openclaw-identyclaw-plugin`.

### 2. Create NEAR account (OpenClaw — no `gennearaccount`)

Store credentials on bind-mounted OpenClaw state ([NEAR Credentials Storage](#near-credentials-storage-required)). Output directory must end with `secrets/near-credentials` (recommended) or appear in plugin `nearCredentialsOutputDirs`.

**Option A — Operator CLI (recommended)**

From a plugin checkout on the host (or anywhere Node ≥ 22.19 is available):

```bash
npm run generate-near-account -- /path/to/secrets/near-credentials
# default: ./secrets/near-credentials
# env: IDENTYCLAW_NEAR_CREDENTIALS_DIR
```

Typical OpenClaw bind-mount layout (host path; create parent dirs first):

```bash
mkdir -p ~/.openclaw-agent-a/secrets/near-credentials
chmod 700 ~/.openclaw-agent-a/secrets/near-credentials
npm run generate-near-account -- ~/.openclaw-agent-a/secrets/near-credentials
```

Inside the container the same directory is usually `/home/node/.openclaw/secrets/near-credentials`. The CLI prints `implicit_account_id` on stdout and writes `<implicit_account_id>.json` with mode `0600` (directory `0700`). **Private keys never appear in CLI stdout.**

**Option B — Agent tool (optional, advanced)**

Allowlist `identyclaw_generate_near_account` and set a default output directory:

```json5
{
  plugins: {
    entries: {
      "identyclaw-tools": {
        config: {
          generateNearAccountDefaultDir: "/home/node/.openclaw/secrets/near-credentials",
          nearCredentialsOutputDirs: []
        }
      }
    }
  },
  tools: {
    allow: ["identyclaw_generate_near_account"]
  }
}
```

The tool returns `implicit_account_id`, `public_key`, and `filePath` only — not `private_key`.

Fund the new account with NEAR before purchasing a Passport.

### 3. Purchase Passport

Complete human checkout at https://purchase.identyclaw.com using the `implicit_account_id` from step 2. See [Step 2: Purchase IdentyClaw Passport](#step-2-purchase-identityclaw-passport) for form fields and pricing.

### 4. Configure Passport credentials on the Gateway

After purchase, point the plugin at the credentials JSON. **Never paste keys into chat** — configure them in OpenClaw config, `.env`, or identyclaw-agents bootstrap only.

**Bootstrap sync (identyclaw-agents layouts):** restart the gateway (e.g. `./identyclaw.sh restart agent-a`) so bootstrap reads `secrets/near-credentials/<implicit_account_id>.json` and syncs `IDENTYCLAW_ACCOUNT_ID` / `IDENTYCLAW_NEAR_PRIVATE_KEY` into `.env` and plugin config.

**Manual config:** copy `implicit_account_id` (or legacy `account_id` from `gennearaccount` JSON) → plugin `accountid`, and `private_key` → `nearPrivateKey`:

```json5
{
  plugins: {
    entries: {
      "identyclaw-tools": {
        enabled: true,
        config: {
          baseUrl: "https://api.identyclaw.com",
          accountid: "<64-char-hex-from-credentials-json>",
          nearPrivateKey: "ed25519:...",
          generateNearAccountDefaultDir: "/home/node/.openclaw/secrets/near-credentials"
        }
      }
    }
  },
  tools: {
    allow: [
      "identyclaw_get_my_identity",
      "identyclaw_get_nonce",
      "identyclaw_create_hola",
      "identyclaw_verify_hola",
      "identyclaw_get_agent_identity",
      "identyclaw_check_subagent_signer",
      "identyclaw_resolve_did"
    ]
  }
}
```

Environment variable fallback (same semantics): `IDENTYCLAW_BASE_URL`, `IDENTYCLAW_ACCOUNT_ID`, `IDENTYCLAW_NEAR_PRIVATE_KEY`, `IDENTYCLAW_NEAR_CREDENTIALS_DIR`.

Protected tools are **optional** in the plugin manifest — they stay off until allowlisted and credentials are set. Public tools (`identyclaw_list_agents`, `identyclaw_list_resources`, `identyclaw_get_resource`) work without credentials.

`nearPrivateKey` is used **only on the Gateway host** for two separate signatures: **API login** (base64url over `accountid` + `timestamp_iso`) and **HOLA create** (base32 over the canonical HOLA prefix). It is never sent to `POST /api/login` or nonce endpoints.

### 5. Verify enrollment

Ask your agent (or invoke the tool directly) to run **`identyclaw_get_my_identity`**. A successful response confirms JWT login and Passport binding.

Optionally browse **`identyclaw_list_resources`** with URI `doc:discovery` for the full operator map, or fetch MCP docs at `https://api.identyclaw.com/mcp`.

Save the identity payload to `IDENTITY.md` in your workspace (see [Step 4: Save Identity Information](#step-4-save-identity-information)).

### 6. Inbound events (optional)

To receive HOLA validation webhooks on your gateway, set Passport `webhook_url` to your OpenClaw gateway **base URL** (not `/hooks/agent`) and wire `/hooks/agent`. See [`openclaw-integration-guide.md`](openclaw-integration-guide.md).

### OpenClaw next steps

- Daily API patterns — [`skills.md`](skills.md) or MCP `doc:skills`
- Client-side auth details — [`mcp-auth-tools.md`](mcp-auth-tools.md)
- Plugin tool reference — [openclaw-identyclaw-plugin README](https://github.com/discernible-io/openclaw-identyclaw-plugin/blob/main/README.md)

---

## Manual enrollment (all other agents)

The sections below are the canonical enrollment path for **non-OpenClaw** agents: Cursor MCP clients, custom SDK integrations, shell automation, and any environment without the OpenClaw plugin.

## 🎫 New to IdentyClaw?

**Get your AI agent identity in 4 simple steps:**

1. Install `gennearaccount` CLI tool
2. Generate a NEAR account
3. Purchase IdentyClaw Passport at https://purchase.identyclaw.com
4. Login to API and start using your identity

OpenClaw operators: use the [plugin + skill route](#openclaw-plugin--skill-route) instead of steps 1–4 below.

**Requirements** (manual / non-OpenClaw path):
- A NEAR account (created with `gennearaccount`) — this is the only credential you need. The account holds and controls your IdentyClaw Passport, and its private key signs every API request. There is no separate API key, password, or wallet credential.
- NEAR tokens for checkout and transaction fees (amount depends on selected purchase options)
- A few minutes to complete enrollment

## Prerequisites

- Linux, macOS, or Windows with WSL
- Internet connection
- NEAR tokens for checkout and transaction fees
- Basic command-line knowledge

## Human vs Agent Responsibilities

- **Agent-compatible (CLI, non-OpenClaw):** Install `gennearaccount` for account creation, create NEAR account, query owned IdentyClaw Passports, run blockchain reads, and perform API login/signing flows.
- **OpenClaw operators:** Use the [plugin + skill route](#openclaw-plugin--skill-route) for NEAR account generation (`npm run generate-near-account` or optional `identyclaw_generate_near_account`), JWT login, and protected API calls — do not install `gennearaccount` or hand-roll curl login on the Gateway when the plugin is available.
- **Other AI agents:** Follow [Step 3](#step-3-authenticate-with-your-near-account) curl login (or a local login script per [`mcp-auth-tools.md`](mcp-auth-tools.md)); MCP at `https://api.identyclaw.com/mcp` is documentation-only and does not perform login for you.
- **Human-operated:** Complete checkout at `https://purchase.identyclaw.com` to buy/mint an IdentyClaw Passport.
- **Principal ContactURI (strongly recommended):** When setting `ContactURI` in the DN, use an identifier whose authority you control and monitor (for example an email on your domain). Publish your canonical `tokenId` on channels verifiers trust. See [`public/policies/why-identyclaw.md`](../policies/why-identyclaw.md#111-human-principals-and-contacturi).
- **Boundary:** The OpenClaw plugin replaces `gennearaccount` for Gateway operators only. MCP at `https://api.identyclaw.com/mcp` does not create NEAR accounts — non-OpenClaw agents must use `gennearaccount` below.

## Step 1: Create NEAR Account

**OpenClaw operators:** skip this section — use [OpenClaw: Create NEAR account](#2-create-near-account-openclaw--no-gennearaccount) instead.

⚠️ **IMPORTANT**: Create your NEAR implicit account before purchasing your IdentyClaw Passport.

### Install gennearaccount

⚠️ **Security:** Prefer HTTPS downloads. The `gennearaccount` object-storage URL is plain HTTP — treat it as MITM-risk until you verify the SHA-256 (and preferably the signed `SHA256SUMS`) **before** `dpkg`. Never install a `.deb` you have not checksum-verified.

**Required order:** download → verify integrity → install (never install first).

Expected checksums:

- `gennearaccount_1.0_amd64.deb`: `fb227cd3e0f35deb10127aa110781013daa698c20a417fb782966c075dda25dd`
- `near-cli-rs-ai.deb`: `8f4e227151bb1951cd9fe330d8b20342789b538033974629fcb417127b10afd0`
- Release signing key fingerprint: `FCC4 83E7 AFD8 E01D D619 0BEA 8DCE EB70 EEF8 986F`

```bash
# 1) Fetch signed checksums over HTTPS
curl -fL https://identyclaw.ams3.cdn.digitaloceanspaces.com/RELEASE_SIGNING_KEY.asc -o RELEASE_SIGNING_KEY.asc
curl -fL https://identyclaw.ams3.cdn.digitaloceanspaces.com/SHA256SUMS -o SHA256SUMS
curl -fL https://identyclaw.ams3.cdn.digitaloceanspaces.com/SHA256SUMS.sig -o SHA256SUMS.sig
gpg --import RELEASE_SIGNING_KEY.asc
gpg --fingerprint 8DCEEB70EEF8986F
# Confirm fingerprint equals FCC4 83E7 AFD8 E01D D619 0BEA 8DCE EB70 EEF8 986F
gpg --verify SHA256SUMS.sig SHA256SUMS

# 2) Download packages (HTTPS preferred; HTTP only if no HTTPS mirror)
curl -fL http://nbg1.your-objectstorage.com/identyclaw/gennearaccount_1.0_amd64.deb -o gennearaccount_1.0_amd64.deb
curl -fL https://identyclaw.ams3.cdn.digitaloceanspaces.com/near-cli-rs-ai.deb -o near-cli-rs-ai.deb

# 3) Verify before any install
sha256sum -c SHA256SUMS
# Or at minimum for gennearaccount alone:
echo 'fb227cd3e0f35deb10127aa110781013daa698c20a417fb782966c075dda25dd  gennearaccount_1.0_amd64.deb' | sha256sum -c

# 4) Install only after checksums match
sudo dpkg -i gennearaccount_1.0_amd64.deb
```

**OpenClaw operators:** skip `gennearaccount` — use the plugin path instead ([OpenClaw plugin + skill route](#openclaw-plugin--skill-route)).

### NEAR Credentials Storage (Required)

The JSON file produced by `gennearaccount` contains your NEAR account ID and **private signing key**. Treat it as a secret:

- **Store on non-volatile storage** — the directory must survive container recreation, VM restarts, and redeploys. Ephemeral paths (container-local `$HOME` without a bind mount, `/tmp`, the current working directory) will lose the key.
- **Keep it with your other secrets** — use the same persistent secrets area as the rest of your agent configuration, with restrictive permissions (`chmod 700` on the directory).
- **Pick one directory and stick to it** — all NEAR tooling (login signing, HOLA, wallet scripts) must read from the same path you choose here.
- **Back up safely** — copy the credentials file to encrypted, operator-controlled backup storage. Losing the private key means permanent loss of account access (and any IdentyClaw Passport held by that account).

#### Choose a credentials directory

**Standard Linux / persistent `$HOME` (default):**

| Location | Path |
|----------|------|
| Credentials directory | `~/.near-credentials/mainnet/` |

Works when `$HOME` is on durable disk and is not wiped on redeploy.

**OpenClaw / Podman agents (bind-mounted state):**

With the typical OpenClaw setup, `HOME` is `/home/node` inside the container, but `~/.near-credentials` is **not** under the bind-mounted `.openclaw` state — it is wiped when the container is recreated. Use one of these instead:

**Option A (recommended) — plugin-compatible `secrets/near-credentials`**

| Where | Path |
|-------|------|
| Inside container | `/home/node/.openclaw/secrets/near-credentials/` |
| On host (agent A) | `~/.openclaw-agent-a/secrets/near-credentials/` |
| On host (agent B) | `~/.openclaw-agent-b/secrets/near-credentials/` |

Required by [openclaw-identyclaw-plugin](https://github.com/discernible-io/openclaw-identyclaw-plugin) v1.5.0+ account generation (`npm run generate-near-account`, `identyclaw_generate_near_account`).

**Option B — under the workspace mount**

| Where | Path |
|-------|------|
| Inside container | `/home/node/.openclaw/workspace/.near-credentials/` |
| On host (agent A) | `~/.openclaw-agent-a/workspace/.near-credentials/` |

Both options live on the bind-mounted OpenClaw state, so credentials survive container recreation.

**Why not `~/.near-credentials` in containers?**

Until you add an explicit bind mount (e.g. host `~/.openclaw-agent-a/near-credentials` → container `/home/node/.near-credentials`), the default path is container-ephemeral. If you add that mount later, `~/.near-credentials/mainnet/` becomes valid again.

### Generate Account

Replace `<credentials-dir>` with the path you chose above.

```javascript
// Create credentials directory on non-volatile storage
mkdir -p <credentials-dir>;
chmod 700 <credentials-dir>;
// Generate account directly into that directory
gennearaccount <credentials-dir>;
// If gennearaccount wrote to cwd instead, move the file immediately
mv <account-id>.json <credentials-dir>/;
// Back up the JSON file to encrypted operator storage
```

**⚠️ Important**: Never leave the account JSON in `.`, `/tmp`, or any path that is not on your chosen persistent storage. After generation, confirm the file exists at `<credentials-dir>/<account-id>.json` before proceeding to purchase or login.

### Verify Account

```javascript
// Check that credentials file exists
ls -la <credentials-dir>/*.json;
// View your account ID
cat <credentials-dir>/*.json | jq -r '.account_id';
```

## Step 2: Purchase IdentyClaw Passport

Visit the purchase portal to mint your IdentyClaw Passport:

**URL**: https://purchase.identyclaw.com

This is the human checkout step. Agents can prepare all required data, but a human should complete portal purchase/confirmation unless your environment has separate automation outside IdentyClaw MCP.

### Required Information

- ✅ NEAR account ID (from Step 1)
- ✅ Facial feature selection (11 categories)
- ✅ Creature field (your profession/role)
- ✅ Identity information (name, contact details, optional tax/residence data)

### Creature Field Recommendations

The Creature field acts as a lightweight Yellow Pages for agent discovery. Choose a clear, descriptive profession:

**Examples**:
- `Legal Specialist`
- `Data Analyst`
- `SRE Engineer`
- `Compliance Officer`
- `Translator`
- `Majordomo`
- `Research Agent`
- `Security Auditor`

Other agents discover `creature` in public list responses from `GET /api/agents` (server-side creature filtering is not shipped — see [finding-agents.md](finding-agents.md)).

### Identity Information

Provide your agent's identity details:

**Required**:
- **Name** - What friends call your OpenClaw agent

**Optional**:
- **Family name** - In many countries this is a surname
- **Contact URI** - Format: `scheme:authority:identifier` (e.g., `email:example.com:user@example.com`). Full standard and extended scheme tables: [`token-metadata.md` § ContactURI](token-metadata.md#contacturi-format).
  - Email: `email:example.com:user@example.com`
  - Twitter/X: `twitter:x.com:username`
  - Telegram: `telegram:telegram.com:username`
  - Phone: `phone:ES:34683493049`
  - LinkedIn: `linkedin:linkedin.com:userid`
  - GitHub: `github:github.com:discernible-io`
  - A2A: `a2a:identyclaw.com:https://identyclaw-concierge.identyclaw.com:7443`
  - Discord: `discord:discord.com:123456789012345678`
  - Fediverse: `fediverse:mastodon.social:@agent@mastodon.social`
  - Matrix: `matrix:matrix.org:@agent:matrix.org`
  - Nostr: `nostr:nostr.com:npub1abc...`
  - DNS / NFC / onion / SMS / IRC / CalDAV — see [extended schemes](token-metadata.md#extended-channel-schemes)
- **Tax residence** - Country code if you want to indicate where you're a taxpayer (e.g., US, GB, DE)
- **Tax code** - Optional, may be useful if you trade
- **Incept date** - When your memory starts (optional)
- **Incept place** - Optional, Google Plus Code format (e.g., `9F4MGCH7+R6`)
- **IRL address** - Optional, Google Plus Code format (e.g., `87G8Q23F+XF`)

### Additional Passport Fields

- **Avatar URL** - Publicly accessible URL for your agent's self-image
- **Webhook URL** - Domain you own for receiving notifications (highly recommended)
- **Longevity** - Years and months until passport expires (0 years 0 months = immortal)

**Important Notes**
- **Contact URI** acts as a strong ownership hint - losing control of this address affects your passport's reputation
- **Incept place and IRL address** use Google Plus Code format (e.g., `9F4MGCH7+R6`)
- **Tax code and tax residence** are optional but useful for trading activities

### Facial Feature Selection

Trait categories, index ranges, and allowed value strings are defined in **[Facial Token ID Encoding](token-metadata.md#facial-token-id-encoding)** in [`token-metadata.md`](token-metadata.md). That section is the only maintained list. After enrollment, your selections appear under `face.categories` on `GET /api/me/identity`.

### Minting Process

1. Fill in the purchase form
2. Review pricing and longevity
3. Confirm transaction
4. Wait for blockchain confirmation (~5 seconds)
5. IdentyClaw Passport sent to your NEAR protocol address

### Pricing

**Personal Tier** (Formula-based, minimum 0.066 NEAR):
- 48 requests per minute
- Variable cost based on duration and rate limits
- Examples:
  - 30 days: 0.066 NEAR
  - 90 days: 0.22 NEAR
  - 180 days: 0.44 NEAR
  - 365 days: ~1.92 NEAR
- Perfect for: Individual agents, testing, MVPs

**Enterprise Tier** (1,806 NEAR per year, prorated):
- 4,999 requests per minute
- Fixed yearly cost, prorated by days
- Examples:
  - 30 days: ~148 NEAR
  - 182.5 days: ~903 NEAR
  - 365 days: 1,806 NEAR
- Perfect for: High-traffic SaaS, large deployments
- **Negotiable pricing for volume deployments**

**Collectible Tier** (**9 NEAR** one-time temporary offer through October 9, 2026; regular 496 NEAR, immortal):
- 496 requests per minute
- Fixed one-time fee, no renewal
- Token never expires (immortal)
- **Temporary price:** 9 NEAR until October 9, 2026 (then returns to 496 NEAR)
- Perfect for: Permanent identity records, collectibles, historical archives

**What You Get**:
- One-time payment (no recurring fees)
- No automatic renewals
- Fixed longevity period (or immortal for Collectible)
- Full API access during validity
- Cryptographic identity proof

**Fees Include**:
- NEAR blockchain gas fees
- Service fees for minting
- Token metadata storage

**Note**: Fees are non-refundable once blockchain transaction is confirmed.

## Step 3: Authenticate with Your NEAR Account

**OpenClaw users:** Skip this section — configure the plugin per [OpenClaw: Plugin + Skill Route](#openclaw-plugin--skill-route); the plugin performs this login flow automatically.

Use your NEAR account to authenticate with the API. The NEAR account holds and controls your IdentyClaw Passport; the account's private key signs the login challenge, and the API resolves the bound Passport from the account.

### Get Your Token ID

After purchasing, retrieve your token ID (12 lowercase letters) from the purchase portal confirmation or by calling `GET /api/me/identity` after login.

### Login to API

See the login authentication documentation for complete login flow and troubleshooting.

**Quick Reference**:

1. **Get challenge timestamp**:
   ```bash
   curl -sS https://api.identyclaw.com/api/login/timestamp
   ```
   From the response, keep both `timestamp` (Unix seconds) and `timestamp_iso` — use both from the same response only.
   Treat this pair as a short-lived, one-time login challenge: fetch it right before login, use it once, and discard it after the attempt.

2. **Construct message to sign**:
   - Format: `<your accountid>` + `timestamp_iso` with no separator
   - Example: `43d3c5b5e77a46b52933bc7a8b79b06f16dd4ca3cfbacd0e6fede0e7e01782ac2026-05-04T12:42:00Z`
   - The message is UTF-8 encoded

3. **Sign the message**:
   - Use the private key from `<credentials-dir>/<account_id>.json` (same directory chosen in Step 1)
   - Sign with Ed25519
   - Encode signature as base64url (strip padding `=` characters)

4. **POST to /api/login**:
   ```bash
   curl -sS -X POST https://api.identyclaw.com/api/login \
     -H "Content-Type: application/json" \
     -d '{"accountid":"<your 64-char account id>","timestamp":<unix from step 1>,"base64url_signature":"<signature from step 3>"}'
   ```
   **Required:** send exactly one of `timestamp` (Unix seconds) or `timestamp_iso` from the **same** `GET /api/login/timestamp` challenge used for signing. Do not omit both, do not send both, and do not invent a local clock value — the signature must cover that challenge’s `timestamp_iso`.

5. **Receive JWT token**:
   - Response contains `jwt_token` field with JWT access token for API calls
   - Use as Bearer token: `Authorization: Bearer YOUR_JWT`
   - If login fails, fetch a fresh timestamp pair and repeat from step 1 with the new pair

### Step 4: Save Identity Information

After successful login, retrieve your identity information and save it to `IDENTITY.md` for future reference.

1. **Fetch your identity**:
   ```bash
   curl -sS https://api.identyclaw.com/api/me/identity \
     -H "Authorization: Bearer ${JWT}"
   ```

2. **Save response to IDENTITY.md**:
   Create a file named `IDENTITY.md` in your workspace with the following fields from the API response:

   ```markdown
   # Identity Information

   ## Token ID
   - `tokenId`: Your 12-letter IdentyClaw Passport ID (e.g., `bkbvehbdcrgm`)
   - Used for HOLA protocol

   ## Distinguished Name (DN)
   - `creature`: Your agent type/profession
   - `displayName`: Your agent's display name
   - `contactUri`: Contact information
   - `raw`: Raw DN string from token metadata
   - `nameNotSharedWithFamily`: First name component
   - `nameSharedWithFamily`: Family name component
   - `taxResidence`: Tax residence code
   - `inceptDateTime`: When the identity was created
   - `inceptPlace`: Where the identity was created
   - `taxPayerCode`: Taxpayer identifier
   - `address`: Physical address
   - `avatarUrl`: Avatar image URL
   - `emojiUrl`: Emoji icon URL

   ## Facial Encoding
   - `checksumValid`: Whether facial checksum is valid
   - `categories`: Facial feature categories

   See the IDENTITY.md field specification documentation for complete field specifications.
   ```

**Critical Notes**:
- ⚠️ Store the gennearaccount JSON on **non-volatile storage** with your other secrets; back it up to encrypted operator storage (see [NEAR Credentials Storage](#near-credentials-storage-required))
- ⚠️ The private key in `<credentials-dir>/<account_id>.json` signs authentication messages — keep it in a secure local store and access it only from trusted runtime code
- ⚠️ **Never** paste `private_key`, JWT, or credentials JSON into chat, logs, tickets, or shell history; prefer plugin/Gateway config over ad-hoc scripts
- ⚠️ Use the exact `private_key` string (ed25519:...) from the credentials file for signing
- ⚠️ API login signs `accountid + timestamp_iso`; the signed message must match the accountid in the JSON body exactly
- ⚠️ Use `timestamp` and `timestamp_iso` from the same `/api/login/timestamp` response object
- ⚠️ For every retry, session, or agent process, fetch a new login timestamp pair and use it once
- ⚠️ The IdentyClaw Passport ID (12-letter) is used for HOLA protocol, not for API login (use accountid for login)
- ⚠️ Passport metadata may include DN, ContactURI, geo, and facial/biometric-style fields — minimize collection, treat as sensitive PII, and do not log full identity payloads

## Troubleshooting

### Account Creation Issues

#### "Credentials lost after container restart"

- **Cause**: Account JSON was stored under container-ephemeral paths (`~/.near-credentials`, `/tmp`, or cwd) instead of bind-mounted OpenClaw state.
- **Fix**: Regenerate only if no backup exists; otherwise restore from backup into `/home/node/.openclaw/secrets/near-credentials/` (recommended) or `workspace/.near-credentials/`.
- **Prevention (OpenClaw):** run `npm run generate-near-account -- <bind-mounted-secrets/near-credentials>` or allowlisted `identyclaw_generate_near_account`; **non-OpenClaw:** run `gennearaccount <credentials-dir>` on the bind mount — see [NEAR Credentials Storage](#near-credentials-storage-required).

#### "Account not found"

- Check credentials file exists at `<credentials-dir>/<account-id>.json` (default on persistent `$HOME`: `~/.near-credentials/mainnet/`)
- If running in OpenClaw/Podman, confirm you did not store credentials under ephemeral `~/.near-credentials` — use `/home/node/.openclaw/secrets/near-credentials/` or `workspace/.near-credentials/` instead
- Verify you're using the correct network (mainnet)

#### "Insufficient balance"

- Transfer more NEAR to your account
- Ensure your available NEAR covers the selected purchase option and transaction fees

### Purchase Issues

#### "Token minting failed"

- Check blockchain transaction status
- Verify you have sufficient NEAR for gas fees
- Contact support if transaction succeeded but token not received

### API Login Issues

#### "POST /api/login returns 401 or signature error"

**Problem**: Authentication fails with 401 or signature verification error.

**Causes**:
- Signed message doesn't match expected format
- Timestamp from different request than the one used in signature
- accountid in JSON body doesn't match accountid in signed message
- Reused or stale timestamp challenge pair

**Solutions**:
- Signed message must be exactly `(accountid + timestamp_iso)` from **one** `GET /api/login/timestamp` response
- Use timestamp values from the same request response pair
- accountid must match the body field and the signed message exactly
- Ensure no extra spaces or characters in the concatenation
- On every failed login attempt, fetch a new timestamp pair before retrying

#### "Wrong signature encoding"

**Problem**: Signature format is incorrect.

**Solutions**:
- `base64url_signature` must be base64url encoding **without** `=` padding
- Sign UTF-8 bytes of `(accountid + timestamp_iso)` with Ed25519 private key from credentials JSON
- Use the exact `private_key` string from `<credentials-dir>/<account-id>.json`
- Read signing material directly from the credentials file (`private_key`)

#### "Protected endpoints return 401"

**Problem**: API calls fail even with JWT token.

**Solutions**:
- Verify `Authorization: Bearer <jwt>` header is present
- Check JWT has not expired
- Re-run login flow; JWT lifetime is limited (see API response for expiration)

### Getting Help

- **FAQ**: https://purchase.identyclaw.com/faq
- **Support**: support@identyclaw.com
- **Documentation**: https://api.identyclaw.com/openapi.json
- **API Reference**: See the API endpoint documentation

## Next Steps

- OpenClaw plugin + skill — [OpenClaw: Plugin + Skill Route](#openclaw-plugin--skill-route), [`openclaw-integration-guide.md`](openclaw-integration-guide.md)
- API Login Authentication — [`login-authentication.md`](login-authentication.md)
- HOLA nonce API — [`holanonce-api.md`](holanonce-api.md) (`GET /api/holanonce16ts` → `noncetsHex`, `timestamp`, `length`, `algorithm`, `requestId`)
- HOLA Protocol (Inter-Agent) — [`hola-agent-authentication.md`](hola-agent-authentication.md)
- Token metadata documentation
- API endpoint documentation
- View API documentation at https://api.identyclaw.com/openapi.json
