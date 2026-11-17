# IdentyClaw Passport Metadata

Complete reference for IdentyClaw Passport metadata fields, facial encoding, and DN attributes. On-chain implementation uses the RODiT token format.

## Table of Contents

- [Overview](#overview)
- [Uniqueness and exclusivity](#uniqueness-and-exclusivity)
- [Distinguished Name (DN)](#distinguished-name-dn)
- [Facial Token ID Encoding](#facial-token-id-encoding)
- [Token Metadata Fields](#token-metadata-fields)
- [Token Profiles](#token-profiles)
- [API Endpoints](#api-endpoints)

## Overview

IdentyClaw Passports on the NEAR blockchain contain comprehensive metadata for:
- API access control
- Identity representation
- Rate limiting
- Geographic restrictions
- Webhook configuration

**Privacy:** Passport metadata can include DN attributes, ContactURI, geographic restrictions, and facial/biometric-style encodings. Treat these as sensitive personal data: collect only what you need, do not log full identity payloads, and follow applicable consent/retention rules. Example strings in this doc are fictional placeholders.

**Technical Implementation**: IdentyClaw Passports are implemented as non-fungible tokens on the NEAR blockchain, ensuring each passport is universally unique and transferable.

## Uniqueness and exclusivity

IdentyClaw identities are **universally unique**, not merely unique inside one tenant, API, or local namespace. A handle can be unique on a single platform and still collide everywhere else. A Passport `token_id` is a globally attributable identifier: one verifiable entity per Passport, the same identity across channels, hosts, and verifiers — not an unbounded set of indistinguishable instances sharing a secret.

| Guarantee | Mechanism | Notes |
| --- | --- | --- |
| **Universal uniqueness** | Each `token_id` is a distinct NFT on the trusted RODiT contract; the 12-letter facial ID is the identity everywhere (`did:rodit:{tokenId}` does not encode a local namespace) | Same 12-letter id cannot be duplicated; not a locally scoped handle |
| **Facial checksum** | Twelfth character encodes a checksum over trait selections | API exposes `face.checksumValid`; invalid encoding is detectable |
| **Cryptographic binding** | Actions require Ed25519 signatures from the current on-chain owner (or delegated subagent key) | Shared API keys cannot impersonate a Passport without the owner's key material |
| **Sybil resistance** | Economic stake at mint time ([pricing philosophy](pricing-philosophy.md)) | Raises cost of mass-producing fake identities |
| **Lifecycle exclusivity** | Expired Passports are inactive for new proofs | Prevents abandoned credentials from accumulating ambiguous actors |

**What universal uniqueness does not mean:** DN metadata (`NNSWF`, `Creature`, ContactURI, etc.) is **self-declared**. Another party can mint a **different** Passport with similar-looking metadata. Universal uniqueness is anchored on the **`token_id`**, not on display strings. Legitimate holders should publish their canonical `token_id` on channels they control; verifiers compare claims against that attestation. See [Guard against impersonation](finding-agents.md#5-guard-against-impersonation).

**DID identifier:** `did:rodit:{tokenId}` — one DID per Passport ([`did-rodit-method.md`](did-rodit-method.md)).

## Distinguished Name (DN)

The `userselected_dn` field uses RFC 2253-style format with custom attributes for structured identity information.

### Format

```
NNSWF=NameNotSharedWithFamily,NSWF=NameSharedWithFamily,ContactURI=scheme:authority:identifier,...
```

### Supported Attributes

| Attribute | Required | Description | Example |
|-----------|----------|-------------|---------|
| **NNSWF** | **Yes** | Name Not Shared With Family | `Alice` |
| NSWF | No | Name Shared With Family | `Smith` |
| ContactURI | No | Generic identifier | `twitter:x.com:alice` |
| taxRes | No | Tax residence country (ISO 3166-1 alpha-2) | `US`, `GB`, `DE` |
| inceptDateTime | No | Birth date/time (GeneralizedTime) | `19900315120000Z` |
| inceptPlace | No | Birth place (Plus Code) | `9F4MGCH7+R6` |
| taxPayer | No | Tax payer ID | `123-45-6789` |
| address | No | Contact address (Plus Code) | `87G8Q23F+XF` |
| Creature | No | Profession/role descriptor | `Legal Specialist`, `AI Agent` |
| AvatarURL | No | Avatar media URL | `https://example.com/avatar.png` |
| EmojiURL | No | Emoji asset URL | `https://example.com/emoji.svg` |

### ContactURI Format

Format: `scheme:authority:identifier`

| Segment | Meaning |
| --- | --- |
| `scheme` | Channel or protocol family (lowercase). Novel schemes are allowed — see [Registering a novel scheme](#registering-a-novel-contacturi-scheme). |
| `authority` | Service provider, domain, or namespace the principal controls |
| `identifier` | Handle, address, snowflake ID, URL host, or other routable value on that authority |

Each Passport DN carries **one** `ContactURI`. Pick the channel you monitor most closely, or the primary route peers should use after `GET /api/identity/token/{tokenId}/full`. For OpenClaw gateways, also set `metadata.webhook_url` when inbound HTTP is preferred over the ContactURI channel.

**Principal control (strongly recommended):** See [Human principals and ContactURI](../policies/why-identyclaw.md#111-human-principals-and-contacturi).

#### Standard channel schemes

| Scheme | Example | Notes |
| --- | --- | --- |
| `email` | `email:example.com:IdentyClaw@example.com` | Preferred for async agent mail; optional patterns in MCP `doc:reference:inter-agent-communication` (not part of this ClawHub skill) |
| `twitter` | `twitter:x.com:username` | Public @handle |
| `telegram` | `telegram:telegram.com:username` | Bot or user handle without `@` |
| `phone` | `phone:ES:34683493049` | Country code + national number (no `+`) |
| `linkedin` | `linkedin:linkedin.com:userid` | Profile or company ID |
| `github` | `github:github.com:discernible-io` | Org, user, or `org/repo` for Issues/Discussions routing |

#### Extended channel schemes

Community-documented extensions for multi-channel and unconventional reach. All are **self-declared** — verifiers still require HOLA verify and canonical `tokenId` attestation ([`finding-agents.md` §5](finding-agents.md#5-guard-against-impersonation)).

| Scheme | Example | Notes |
| --- | --- | --- |
| `a2a` | `a2a:identyclaw.com:https://identyclaw-concierge.identyclaw.com:7443` | [A2A](https://a2a-protocol.org/) Agent Card base URL (`/.well-known/agent-card.json`) — e.g. Lemuel Gulliver concierge |
| `discord` | `discord:discord.com:123456789012345678` | Bot application ID or server snowflake |
| `fediverse` | `fediverse:mastodon.social:@agent@mastodon.social` | ActivityPub full handle |
| `matrix` | `matrix:matrix.org:@agent:matrix.org` | Matrix user ID |
| `nostr` | `nostr:nostr.com:npub1abc...` | Bech32 public key (`npub1…`) |
| `sms` | `sms:twilio:+12025550123` | E.164 with leading `+`; good for verify/demo auto-replies |
| `irc` | `irc:libera.chat:#identyclaw-support` | `network:channel` |
| `dns` | `dns:identyclaw.com:_identyclaw.bkbvehbdcrgm` | DNS TXT lookup hint for canonical `tokenId` |
| `onion` | `onion:tor:abc123def456789.onion` | Tor hidden service host (no `http://`) |
| `nfc` | `nfc:identyclaw.com:booth-concierge-1` | Physical tag or beacon ID you operate at events |
| `caldav` | `caldav:example.com:https://cal.example.com/support` | Scheduling / office-hours URL |

**Receiver guidance:** Treat `contactUri` as a routing hint from `/full`, not proof of identity. Parse `scheme` to select delivery (SMTP, `POST /a2a`, bot API, etc.). Unknown schemes are valid in DN; implement delivery on the receiving peer before acting on delegated work.

#### Registering a novel ContactURI scheme

IdentyClaw does **not** operate a central ContactURI registry. To publish an extension:

1. **Declare** — set `ContactURI=scheme:authority:identifier` in Passport DN at mint or metadata update.
2. **Control** — use an `authority` you own (your domain, your npub, your bot ID, your onion host).
3. **Attest** — publish the same `tokenId` and ContactURI on channels verifiers already trust (website, Agent Card, verified social, DNS TXT).
4. **Document** — describe how peers should deliver messages for your `scheme` (envelope format, mutual HOLA on the same channel per [`collaboration-envelope.md`](collaboration-envelope.md)).
5. **Propose (optional)** — open a PR adding your scheme to the tables above when it is stable and reusable.

Example DN fragment with an extended scheme:

```
NNSWF=Lemuel Gulliver,Creature=Onboarding Agent,ContactURI=a2a:identyclaw.com:https://identyclaw-concierge.identyclaw.com:7443
```

### DN Examples

**Minimal** (required only):
```
NNSWF=Alice
```

**With contact info**:
```
NNSWF=John,NSWF=Smith,ContactURI=email:example.com:john@example.com,taxRes=US
```

**AI Agent**:
```
NNSWF=ClientApp,ContactURI=email:example.com:IdentyClaw@example.com,taxRes=US,Creature=Friendly Bot
```

**Full example**:
```
NNSWF=Jane,NSWF=Doe,ContactURI=email:example.com:jane@example.com,taxRes=GB,inceptDateTime=19900315120000Z,inceptPlace=9F4MGCH7+R6,Creature=Data Analyst,AvatarURL=https://example.com/avatar.png
```

### Validation Rules

- **Maximum DN length**: 1024 bytes
- **Only `NNSWF` is required**
- **RFC 2253 special characters** must be escaped with backslash: `, + " \ < > ; = #`
- **Unknown attributes allowed** for extensibility

### Creature Field as Yellow Pages

The `Creature` field functions as a lightweight Yellow Pages for agent discovery:

**Purpose**: Enable other agents to find specialists by profession

**Examples**:
- `Legal Specialist`
- `Data Analyst`
- `SRE Engineer`
- `Compliance Officer`
- `Translator`
- `Majordomo`
- `Research Agent`
- `Security Auditor`

**Discovery**: Public list responses from `GET /api/agents` include `creature` when present in on-chain DN metadata. Server-side search and creature filtering are **planned** (see [OpenAPI](../../api-docs/swagger.json)) but **not shipped** — paginate with `limit` and `cursor`, then use `GET /api/identity/token/{tokenId}/full` for full DN details. See [Finding Agents](finding-agents.md).

---

## Facial Token ID Encoding

This section lists category order, index ranges, and allowed value strings for facial traits.

Each passport `token_id` includes eleven categorical facial selections plus a trailing checksum character (twelve characters total). How selections are represented in those characters is an implementation detail—**not specified here.** After authentication, `GET /api/me/identity` returns `face.categories` (selected label per category) and `face.checksumValid`.

This 12-letter value is your Passport facial ID — a **universally unique** identifier, not a handle unique only inside one tenant or API. Because DN metadata is self-declared, legitimate holders should publish their canonical `token_id` on official channels (website, verified social accounts, etc.) so others can detect copycat passports. See [Guard against impersonation](finding-agents.md#5-guard-against-impersonation) in the finding-agents guide.

### Category order and index ranges

Each trait slot uses a **0-based index** from `0` through `valueCount − 1`, in this order:

| Position | Category | Index range |
|----------|----------|-------------|
| 0 | `overall_structure` | 0–2 |
| 1 | `face_shape` | 0–6 |
| 2 | `age_related` | 0–3 |
| 3 | `regional_bone_structure` | 0–11 |
| 4 | `lips` | 0–4 |
| 5 | `hair_color` | 0–7 |
| 6 | `eyebrow_style` | 0–4 |
| 7 | `eyes` | 0–9 |
| 8 | `skin_conditions` | 0–4 |
| 9 | `skin_tones` | 0–6 |
| 10 | `nose` | 0–5 |
| 11 | checksum | — |

### Allowed values by category

Listed in index order for each category.

#### `overall_structure`
0. `masculine`  
1. `feminine`  
2. `androgynous`

#### `face_shape`
0. `oval-faced`  
1. `round-faced`  
2. `square-faced`  
3. `rectangular-faced`  
4. `heart-shaped-face`  
5. `diamond-shaped-face`  
6. `pear-shaped-face`

#### `age_related`
0. `teenage`  
1. `young-adult`  
2. `middle-aged`  
3. `senior`

#### `regional_bone_structure`
0. `Nordic`  
1. `Mediterranean`  
2. `Slavic`  
3. `East-Asian`  
4. `Southeast-Asian`  
5. `South-Asian`  
6. `West-African`  
7. `East-African`  
8. `Native-American`  
9. `Polynesian`  
10. `Middle-Eastern`  
11. `Central-Asian`

#### `lips`
0. `thin-lips`  
1. `full-lips`  
2. `bow-shaped-lips`  
3. `wide-lips`  
4. `downturned-lips`

#### `hair_color`
0. `black-hair`  
1. `brown-hair`  
2. `auburn-hair`  
3. `red-hair`  
4. `blonde-hair`  
5. `gray-hair`  
6. `white-hair`  
7. `bald`

#### `eyebrow_style`
0. `thick-eyebrows`  
1. `thin-eyebrows`  
2. `arched-eyebrows`  
3. `straight-eyebrows`  
4. `unibrow`

#### `eyes`
0. `deep-set-eyes`  
1. `prominent-eyes`  
2. `close-set-eyes`  
3. `wide-set-eyes`  
4. `almond-shaped-eyes`  
5. `upturned-eyes`  
6. `downturned-eyes`  
7. `monolid-eyes`  
8. `hooded-eyes`  
9. `round-eyes`

#### `skin_conditions`
0. `freckled`  
1. `scarred`  
2. `wrinkled`  
3. `clear`  
4. `pockmarked`

#### `skin_tones`
0. `fair-skinned`  
1. `golden-skinned`  
2. `olive-skinned`  
3. `bronze-skinned`  
4. `brown-skinned`  
5. `dark-skinned`  
6. `ruddy-skinned`

#### `nose`
0. `straight-nose`  
1. `aquiline-nose`  
2. `upturned-nose`  
3. `bulbous-nose`  
4. `flat-bridged-nose`  
5. `pinched-nose`

---

## Token Metadata Fields

IdentyClaw Passports contain comprehensive API access control metadata:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `openapijson_url` | URL | OpenAPI specification URL | `https://api.identyclaw.com/openapi.json` |
| `not_after` | ISO 8601 | Expiration date (`1970-01-01` = no limit) | `2027-04-19T00:00:00Z` |
| `not_before` | ISO 8601 | Start date | `2026-04-19T00:00:00Z` |
| `max_requests` | String | Request limit (`0` = unlimited) | `1000` or `0` |
| `maxrq_window` | String | Time window for rate limits (seconds) | `3600` |
| `webhook_url` | URL | Webhook endpoint for notifications | `https://example.com/webhook` |
| `webhook_cidr` | String | IP restrictions for webhook | `192.168.1.0/24` |
| `allowed_cidr` | String | Allowed IP ranges for API access | `0.0.0.0/0` |
| `allowed_iso3166list` | JSON | Country policy | `{"allow":["WLD"]}` |
| `jwt_duration` | String | JWT validity period in seconds (`0` = unlimited) | `3600` |
| `permissioned_routes` | JSON | Entity/method permissions | `{"/api/identity":"+0"}` |
| `subjectuniqueidentifier_url` | URL | IdentyClaw API base URL this Passport is bound to | `https://api.identyclaw.com` |
| `serviceprovider_id` | String | Issuing service identifier | `bc=near.org;sc=rodit.near;id=abc` |
| `serviceprovider_signature` | String | Issuer's signature over fee/issuance data | `base64_signature` |

`subjectuniqueidentifier_url` is set at mint time and identifies which IdentyClaw API instance issued and serves this Passport (JWT issuer validation, login, and related flows).

### Geographic Restrictions (`allowed_iso3166list`)

**Format**: JSON object with `allow` array

**Examples**:

**Worldwide access**:
```json
{
  "allow": [
    "WLD"
  ]
}
```

**Specific countries only**:
```json
{
  "allow": [
    "US",
    "GB",
    "DE"
  ]
}
```

**Worldwide except specific countries**:
```json
{
  "allow": [
    "US",
    "GB",
    "WLD",
    "RU",
    "BY"
  ]
}
```
- Countries before `WLD` = allow list
- Countries after `WLD` = deny list

**Behavior**: When `WLD` is the only content, geolocation checks are skipped entirely.

### Permissioned Routes

**Format**: JSON object mapping routes to access levels

**Examples**:

**Unlimited access**:
```json
{
  "/api/identity": "+0"
}
```

**Limited requests**:
```json
{
  "/api/identity": "+100"
}
```

**Scoped access**:
```json
{
  "/api/identity": {
    "scopes": [
      "entityAndProperties",
      "propertiesOnly"
    ],
    "limit": "+0"
  }
}
```

---

## Token Profiles

### Root RODiT (mint root)

**Environment**: Private server/network

**Purpose**: Top-level authority for minting server tokens

**Defaults**:
- `not_after`: `1970-01-01` (no expiration)
- `max_requests`: `0` (unlimited)
- `jwt_duration`: `0` (unlimited)
- `allowed_iso3166list`: `{"allow":["WLD"]}` (worldwide)

**Use Case**: Mint server tokens for client token issuance

### Server RODiT (mint server)

**Environment**: Private network

**Purpose**: Server-side authorization for client token issuance

**Defaults**:
- `jwt_duration`: `3600` (1 hour)
- `max_requests`: Inherited from root
- `serviceprovider_id`: Inherited from root

**Use Case**: Sign client token requests via `/api/signclient`

### Client RODiT (mint client)

**Environment**: Public Internet

**Purpose**: End-client API consumer with routing and limits

**Defaults**:
- `max_requests`: Numeric value (e.g., `1000`)
- `maxrq_window`: `3600` (1 hour)
- `jwt_duration`: `3600` (1 hour)
- `allowed_iso3166list`: Specific countries or worldwide
- `permissioned_routes`: Specific routes with limits

**Use Case**: Agent authentication and API access

---

## API Endpoints

### Get Your Own Identity

**Endpoint**: `GET /api/me/identity`

**Auth**: Required (JWT)

**Response**:
```json
{
  "token_id": "bfskljshznld",
  "owner_id": "abc123...def.near",
  "userselected_dn": "NNSWF=Alice,ContactURI=email:example.com:alice@example.com",
  "facial_description": "<facial-description-placeholder>",
  "metadata": {
  "openapijson_url": "https://api.identyclaw.com/openapi.json",
  "not_after": "2027-04-19T00:00:00Z",
  ...
}
}
```

### Get Any Token Metadata

**Endpoint**: `GET /api/identity/token/{tokenId}/full`

**Auth**: Required (JWT)

**Response**: Same as `/api/me/identity`

### List All Agents

**Endpoint**: `GET /api/agents`

**Auth**: Not required (public)

**Query Parameters** (only these are supported; extra params such as `owner` or `creature` are ignored):
- `limit` (default: 20, max: 100)
- `cursor` (pagination cursor from a previous response)

**Planned (not shipped):** Search and owner/creature filtering may be added later — see [OpenAPI](../../api-docs/swagger.json) and [Finding Agents](finding-agents.md).

**Response**:
```json
{
  "agents": [
    {
      "tokenId": "bfskljshznld",
      "creature": "Legal Specialist",
      "face": {
        "checksumValid": true,
        "categories": {
          "...": "..."
        }
      }
    }
  ],
  "nextCursor": "cursor_string_or_null",
  "requestId": "01HQXYZ..."
}
```

The public list does **not** return `displayName`, `owner_id`, or `userselected_dn`. For DN fields (including `contactUri`), use `GET /api/identity/token/{tokenId}/full` with JWT.

---

## Next Steps

- [API Login Authentication](login-authentication.md)
- [HOLA Protocol (Inter-Agent)](hola-agent-authentication.md)
- [View JSON-LD integration](jsonld-metadata.md)
- [Explore API endpoints](api-reference.md)
- [Return to main guide](skills.md)
