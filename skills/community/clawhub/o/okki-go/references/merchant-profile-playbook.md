# Merchant Profile Playbook

This playbook defines the long-term Merchant Profile contract used by OKKI Go discovery and outreach workflows. It is a rule contract for `~/.config/okki-go/profile.json` v1.1; implementation details for reading and writing the file belong to `scripts/okki-state.js`.

## Contents

1. Profile Schema
2. Trigger Modes and Lifecycle
3. Discovery Reuse Rules
4. Outreach Reuse Rules
5. Sensitive Fields and Privacy

## 1. Profile Schema

`profile.json` is stored at `${XDG_CONFIG_HOME:-$HOME/.config}/okki-go/profile.json` with file mode `0600`. The schema version is `"1.1"`.

### Field Classes

Fields are split by inference risk.

**A class fields** do not carry `source` metadata. They are values the user must provide directly or confirm explicitly, so they are treated as `user_confirmed`:

- `company.name`
- `company.website`
- `company.country`
- `company.employee_range`
- `company.founded_year`
- `outreach_identity.sender_name`
- `outreach_identity.sender_email`
- `outreach_identity.sender_title`
- `outreach_identity.signature_block`
- `outreach_identity.preferred_language`
- `offerings.primary_products`
- `offerings.landing_page`

**B class fields** must be stored as objects with `value`, `source`, and `updated_at`:

- `offerings.usps`
- `offerings.applications`
- `offerings.certifications`
- `target_baseline.regions_primary`
- `target_baseline.decision_roles`
- `exclusions.industries_blacklist`

### Source States

| Source | Meaning | May Feed Discovery Defaults | Write Rule |
|--------|---------|-----------------------------|------------|
| `user_confirmed` | User explicitly confirmed the value for future reuse. | Yes | Write after the user confirms saving or onboarding answer. |
| `user_provided` | User said the value in-session but did not confirm long-term profile reuse. | Only if no confirmed/imported value exists for that field. | Write only when the user gave the value clearly. |
| `user_provided_current_turn` | User stated the value in the current prospecting request. It is session seed data, not a long-term Profile default. | Yes for the current search or Minimal Prospecting Profile only. | Do not persist unless the user confirms saving. |
| `agent_inferred` | Agent inferred the value and it is waiting for user confirmation. | No | Must be labeled and followed by a confirmation prompt. |
| `imported` | User imported the value from an external system or file. | Yes | Treat as confirmed unless the import UI marks it otherwise. |

`agent_inferred` values must never silently become facts. They can be stored to support later confirmation, but they are excluded from Discovery defaults until the user confirms them.

### Completeness

`completeness` is a number from `0` to `1`. It is computed from the five profile field families and only counts user-confirmed data:

- company identity
- offerings
- target baseline
- outreach identity
- sales context

Completeness drives Progressive Enrichment and the profile confirmation flow. Normal L0 search stays owned by `search-fast-path.md`.

### Dynamic Trade Anchor

`profile.company.country` can help dynamic `trade_mode` inference when the user asks for sales strategy. `trade_mode` itself is not stored in the Profile and must not block L0 Default Search:

```text
trade_mode = derive(profile.company.country, brief.geo_include)
```

When `company.country` is missing, `trade_mode = unknown`; direct free company search may continue under `search-fast-path.md`, but trade-mode-dependent mentor advice must degrade or be deferred.

### Preferred Language Lazy Loading

`outreach_identity.preferred_language` starts as `null` and is not mandatory during Lite Onboarding. The first outreach workflow that needs it may infer a default, present it to the user, and write the confirmed value back as user-confirmed profile data.

Default inference rules:

- `trade_mode = domestic` and `profile.company.country` has a known local language: propose that local language.
- `trade_mode = domestic` and the country is commonly English-speaking: propose `en`.
- `trade_mode = cross_border` and target markets are mainly English-speaking: propose `en`.
- `trade_mode = cross_border` and target markets are mainly non-English-speaking: propose `en` as a common cross-border default and ask whether localization is needed.
- `trade_mode = mixed`: ask the user instead of guessing.
- Unknown or ambiguous cases: ask the user.

### Sales Context

`sales_context` stores optional user-confirmed sales preferences such as `goal`, `time_horizon`, `channel`, `source`, and `updated_at`. L1/L2 mentor advice may read it when useful, but L0 Default Search must not ask Business Context questions before the first free search.

### Example v1.1 Profile

```json
{
  "version": "1.1",
  "updated_at": "2026-05-28T10:00:00Z",
  "completeness": 0.7,
  "company": {
    "name": "Example Manufacturing Co.",
    "country": "CN",
    "type": ["manufacturer"],
    "employee_range": "50-200",
    "founded_year": "2010",
    "website": "https://example.com"
  },
  "offerings": {
    "primary_products": ["DTF printer"],
    "product_keywords_zh": ["数码热转印机", "DTF打印机"],
    "product_keywords_en": ["DTF printer", "direct-to-film printer"],
    "applications": [
      { "value": "custom apparel", "source": "user_confirmed", "updated_at": "2026-05-26" },
      { "value": "promotional gifts", "source": "agent_inferred", "updated_at": "2026-05-28" }
    ],
    "usps": [
      { "value": "Tier-1 components", "source": "user_confirmed", "updated_at": "2026-05-26" },
      { "value": "in-house R&D", "source": "user_provided", "updated_at": "2026-05-26" }
    ],
    "certifications": [
      { "value": "quality management certification", "source": "user_confirmed", "updated_at": "2026-05-26" }
    ],
    "landing_page": "https://example.com/products"
  },
  "target_baseline": {
    "company_types": ["manufacturer", "trading"],
    "regions_primary": [
      { "value": "US", "source": "user_confirmed", "updated_at": "2026-05-26" },
      { "value": "DE", "source": "user_confirmed", "updated_at": "2026-05-26" },
      { "value": "AU", "source": "agent_inferred", "updated_at": "2026-05-28" }
    ],
    "regions_excluded": ["RU"],
    "decision_roles": [
      { "value": "Procurement Manager", "source": "user_confirmed", "updated_at": "2026-05-26" }
    ],
    "employee_range": "50-1000"
  },
  "outreach_identity": {
    "sender_name": "Sender Name",
    "sender_title": "Sales Manager",
    "sender_email": "sender@example.com",
    "signature_block": "Sender Name | Example Manufacturing Co.",
    "preferred_language": null
  },
  "sales_context": {
    "goal": "expand_new_market",
    "time_horizon": "this_quarter",
    "channel": "edm",
    "source": "user_confirmed",
    "updated_at": "2026-05-28"
  },
  "exclusions": {
    "competitor_domains": ["competitor.example"],
    "industries_blacklist": [
      { "value": "restricted industry", "source": "user_confirmed", "updated_at": "2026-05-26" }
    ]
  },
  "history": {
    "last_used_axes": {
      "geo": ["DE", "US"],
      "industry": ["textile printing"],
      "decision_role": ["Procurement Manager"]
    },
    "search_count": 12
  }
}
```

## 2. Trigger Modes and Lifecycle

### Mode 1: Lite Onboarding

Run Lite Onboarding only when the user asks to save or set up reusable Merchant Profile defaults, or when they explicitly want guided profile setup. The user must already have passed the normal API key setup flow before API calls are attempted; onboarding itself does not bypass authentication.

Before asking Lite Onboarding questions, apply current-turn facts from the user request. Do not repeat questions for merchant facts the user already provided. For example, if the user says "我是中国的汽车玻璃制造商", skip L0 company country, L1 company type, and L2 primary product questions for the current session; ask only missing fields such as target market, customer region, decision roles, or whether to save the facts.

Lite Onboarding asks merchant-profile defaults for future reuse. Product Context Lite in `search-strategy.md` asks only what is needed for the current L2 search route. Boundary rules:

- If current-turn facts can build a free search or Minimal Prospecting Profile, skip Lite Onboarding.
- If current-turn facts include product/company type but miss target geography or target route, ask only that current-search missing field.
- If the user says "我是纸品包装制造商，帮我开发潜客", do not ask what product they sell or whether they are a manufacturer; ask which target market or buyer route to develop.
- Ask Lite Onboarding only when the user wants guided setup, future default saving, or there is no usable current-search seed.

Ask exactly five lightweight questions:

1. **L0 company country, required:** "Which country or region does your company mainly operate from?" Write to `profile.company.country`. This is the anchor for future `trade_mode` derivation. Use `api-reference.md` or wrapper normalization for country code details.
2. **L1 company type, required:** manufacturer, trader, service provider, brand owner, or user-specified equivalent.
3. **L2 primary product or service keywords, required:** one to three keywords.
4. **L3 primary customer regions, required:** common options plus custom countries or regions.
5. **L4 usual decision roles, optional:** common role options plus custom roles.

Answers from Lite Onboarding are written as user-confirmed profile data. After L0 and L3 exist, the first `trade_mode` can be derived:

- L3 contains only L0: `domestic`
- L3 excludes L0: `cross_border`
- L3 contains L0 and other markets: `mixed`
- L0 missing: `unknown`

### Mode 2: Progressive Enrichment

At the start of each Prospecting Brief Discovery, compute completeness. If a field family is missing, ask at most one follow-up near the related Gray Area instead of launching another long onboarding flow.

Example prompt:

```text
One quick profile question for future searches: what is the strongest reason customers choose you over alternatives? Examples include quality proof, delivery speed, custom capability, or industry experience. This will not block the current search.
```

When the user answers and agrees to reuse the value, write it as `user_confirmed` and recompute completeness.

### Mode 2.5: Agent Inference Confirmation

When the agent infers a B class value from conversation, it may store the value with `source: "agent_inferred"` and must ask for confirmation before using it as a Discovery default.

Confirmation pattern:

```text
I inferred that your target markets may include SG and MY. Should I add them to your primary markets?
(a) Add both
(b) Add only SG
(c) Do not add them
(d) Let me choose manually
```

If the user accepts or edits the value, change the chosen entries to `user_confirmed`. If the user rejects them, remove the inferred entries. If the user does not answer, keep the inferred entries but exclude them from defaults and clearly mark them in profile views.

### Mode 2.55: Current-Turn Merchant Seed Confirmation

Current-turn facts may be used immediately for the current free search or Minimal Prospecting Profile when the user stated them clearly. They should not become long-term Merchant Profile defaults silently.

Rules:

- Use `user_provided_current_turn` facts to avoid repeated profile questions in the same turn.
- If those facts would improve future defaults, ask after or alongside the search whether to save them.
- If the user confirms saving, write accepted values as `user_confirmed`.
- If the user does not confirm saving, keep them session-only.
- Never downgrade clear current-turn facts to `agent_inferred`.

### Mode 2.6: Website/Product Page Quick Profile

When the user explicitly asks to use a company website or product page for profile setup, any extracted data is provisional until the user confirms it.

Rules:

- Record source URL or pasted-source description where practical.
- Extract company country/region, company type, primary products/services, applications, differentiators, certifications, delivery/customization capability, target-customer clues, and explicit exclusions only when supported by the source.
- Represent unconfirmed extraction as `agent_inferred` or implementation-specific pending session state; do not use it as confirmed Profile defaults.
- Show the extracted profile in a conversational confirmation message before search.
- When the user confirms or edits the extraction, save the accepted fields with `profile upsert --json` and source `user_confirmed`.
- If the user rejects the extraction, do not save rejected fields and do not use them as long-term defaults.

Confirmation means "save locally and use for this search"; no second save prompt is needed when the confirmation text says that explicitly.

### Mode 3: Management Workflow

The skill must support a `Merchant Profile Management` workflow independent of a search request.

Supported operations:

- **View:** show a redacted profile with source labels. Do not print complete `sender_email` or other semi-sensitive fields unless the user explicitly asks to reveal them.
- **Edit:** update any field and mark the new value according to its source state.
- **Reset:** clear and rebuild the profile only after explicit confirmation.
- **Export:** tell the user the local file path and show a redacted preview by default.
- **Import:** accept profile data from a user-provided source and mark imported B class entries as `imported`.

View output must make source status visible:

```text
regions_primary: US (confirmed), DE (confirmed), AU (agent_inferred; not used as default)
sender_email: s***@example.com
```

## 3. Discovery Reuse Rules

Mentor Guided and optional profile reuse read Profile defaults before asking more questions. They must prefer only confirmed or imported long-term data:

- `user_confirmed`: may be presented as default.
- `imported`: may be presented as default.
- `user_provided`: may be used only when no confirmed/imported option exists for the same field, and the prompt must say it came from the current or prior conversation rather than the confirmed profile.
- `user_provided_current_turn`: may feed the current free search, Minimal Prospecting Profile, and target-side projection without a repeated question; it must be confirmed before long-term persistence.
- `agent_inferred`: must not be used as a default.

Default mapping:

| Discovery Area | Profile Source |
|----------------|----------------|
| Merchant offer anchor | `offerings.primary_products`, `offerings.product_keywords_en`, `offerings.product_keywords_zh` |
| Merchant capabilities | confirmed/imported `offerings.usps`, `offerings.certifications`, `offerings.applications` |
| Target route hints | `target_baseline.company_types`, `target_baseline.industries`, target-customer clues from confirmed website extraction |
| Target geography | confirmed/imported `target_baseline.regions_primary` |
| Include geography | confirmed/imported `target_baseline.regions_primary` |
| Exclude geography | `target_baseline.regions_excluded` and relevant `exclusions` |
| Employee range | `target_baseline.employee_range` |
| Decision roles | confirmed/imported `target_baseline.decision_roles` |

Merchant offer terms feed `merchant_offer_anchor` and PMF reasoning. They do not automatically become API `productKeywords`; `search-fast-path.md` or `search-strategy.md` must project them through target-side routes first.

When the user changes a Profile-derived default in the current search or Minimal Prospecting Profile, ask whether the change should update the Profile:

```text
You changed the target markets from US, DE to US, JP. Save this to your Merchant Profile for future defaults?
(a) Yes, update the profile
(b) No, only use it this time
```

Profile defaults never replace current-turn facts or the session Minimal Prospecting Profile.

## 4. Outreach Reuse Rules

Outreach workflows may reuse Profile fields only after the search and contact discovery side of the workflow reaches the existing outreach stage.

Allowed reuse:

- `outreach_identity.signature_block` for email signatures.
- `outreach_identity.sender_name`, `sender_title`, and redacted `sender_email` for draft context.
- `offerings.primary_products` and confirmed/imported `offerings.usps` for value proposition language.
- `outreach_identity.preferred_language`; if `null`, infer and confirm a default before writing it back.
- `sales_context` to guide optional L1/L2 tone, channel preference, and first-touch angle when the user asks for advice.

Safety boundary:

- Profile reuse can help draft outreach content.
- Profile reuse cannot skip recipient confirmation.
- Profile reuse cannot skip email content confirmation.
- Profile reuse cannot skip EDM quota confirmation or any paid-action confirmation.
- Workflow C keeps the existing email confirmation and send flow after the company/contact discovery front half.

## 5. Sensitive Fields and Privacy

`profile.json` is local state and must be mode `0600`.

Privacy rules:

- Never store API keys in `profile.json`.
- Never report `sender_email`, `sender_name`, email body, API key, or sensitive profile content in analytics.
- In profile views, redact `outreach_identity.sender_email` and `sender_name` by default.
- Reveal full semi-sensitive fields only when the user explicitly asks.
- When exporting, default to a redacted preview and remind the user of the local file path.
- Make every `agent_inferred` field obvious in profile views so the user can confirm or reject it.

If a future workflow deletes the profile file, it must be an explicit reset action. It must not happen as a side effect of Discovery, Expansion, or outreach.
