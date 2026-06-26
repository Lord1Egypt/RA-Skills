# Research playbook — which tool for which signal

Research quality = breadth × depth × truthfulness. This doc pins down the
mapping so the sub-agent and the main skill behave consistently.

## Signal matrix

For each target, we're hunting for signals in SEVEN dimensions. The first
two (prior conversations, same-company context) often beat any external
research — run them first.

| Dimension | Category (must be `ready`) | Expected output |
|-----------|---------------------------|-----------------|
| **Prior conversations** (with target) | `comms_email`, `comms_chat`, `comms_sms`, `professional_network` | Dates, channels, directions, one-line summaries of past threads. Signatures parsed (inc. image OCR) for phone/title/address. |
| **Same-company context** | KB (local) + `crm` | People in the KB already at this company (titles, warmth, opt-outs). Prior interactions with the org. |
| Recent public activity | `social`, `professional_network`, `research_web` | Specific posts/talks with dates and links |
| Career trajectory | `crm`, `professional_network` | Current role tenure, prior 2 companies with dates |
| Topic interests | `social`, `professional_network`, `research_web` | 2-3 specific topics inferred from what they share/write |
| Mutual connections | `crm`, `professional_network` | Names of 1-3 shared contacts |
| Firmographics (org) | `crm`, `research_web` | Size, funding stage, tech stack, recent news |

## Category-specific recipes

### `crm` — LeadClaw / Leadbay

Primary signal source when available. One query: `leadclaw.get_lead(<query>)`.
Returns the full lead + company record + ICP score + relationship graph.

Also use `leadclaw.search_leads(…)` for discovery intents ("pull a lead worth
talking to"). Filter the returned set by ICP match score and pick the highest
that hasn't been contacted.

### `professional_network` — LinkedIn

Primary signal source for career + recent posts (if social isn't connected).

Key queries via `linkedin-cli` (installed via clawhub):
- Profile by URL → role history, education, about-section (topics)
- Posts by user → most recent 10 posts; keep any ≤30 days as signals
- Mutual connections with user's LinkedIn URL (from `kb/me/self.md`)

### `social` — Twitter/X, Bluesky

Best for voice + current interests. Query recent 20 posts; filter to ≤30 days;
sample 3-5 that best reveal topics. Store URL + date + one-sentence summary.

### `research_web` — browse, summarize, goplaces

The fallback + enrichment layer.

- `browse` the company's blog → surface recent posts that mention the target
  or their team
- `browse` podcast directories / YouTube for talks
- `summarize` long-form content you find into page-sized summaries

### `research_contacts` — apple-notes, apple-reminders, things-mac

Often yields gold: the user already wrote about this person in their own
notes app. Quick check; skip if nothing.

## Required coverage rule

For the quality bar (≥3 concrete recent signals + ≥1 connection point), the
sub-agent MUST query every category in inventory marked `ready`. Skipping a
`ready` category is a quality violation flagged in the eval.

If a category yields nothing, record it as a `gaps[]` entry rather than
silently dropping.

## Connection points — how to find them

Read `kb/me/self.md` and `kb/me/org.md`. Look for overlaps with the target:

- **Mutual orgs**: target's work history ∩ user's work history (including
  user's company's prior hires, board members, investors if listed in
  `me/org.md`).
- **Mutual schools**: education ∩ user's education.
- **Mutual topics**: target's inferred topics ∩ user's listed interests.
- **Mutual connections**: directly listed mutuals (Leadbay graph, LinkedIn).

Rank connection points by strength (1-10):
- 10 = direct warm intro possible (mutual 1st-degree connection)
- 8 = shared company with overlap in time
- 6 = shared school/city/topic with specific hook
- 3 = generic industry overlap

## Email domain classification (non-negotiable)

Before deriving a company from a target's email, run
`python3 shared/scripts/domain_classifier.py "<email>"`. The classifier
returns one of: `private`, `isp`, `school`, `corporate`, `unknown`.

| Class | What it means | What to do |
|-------|---------------|------------|
| `private` | Consumer webmail (gmail.com, hotmail, yahoo, icloud, proton, yandex, …) | **Do NOT use this domain to identify employer.** Rely on LinkedIn / Leadbay / user-stated company. |
| `isp` | Residential internet provider (comcast.net, btinternet.com, …) | Same rule — not employer data. |
| `school` | Academic (.edu, .ac.uk, hec.fr, mit.edu, …) | Academic affiliation (current or former). Record under `## Affiliations`, never as current `company`. |
| `corporate` | Real company domain | Derive `company_slug` via the helper; create/update `kb/orgs/<slug>.md`; link `person → org`. |
| `unknown` | Empty / malformed | Leave empty, log a gap. |

Wrong filings this catches: `alice@gmail.com` → "Gmail" as her company;
`bob@mit.edu` → "MIT" as Bob's current employer (when Bob is actually at
a company and still uses an alumni email).

## Signatures — structured extraction

Email signatures are a goldmine for phone / title / address. The signature
is usually at the BOTTOM of a message separated by `-- ` or a visual rule.
Extract into structured fields on the KB frontmatter, not into prose:

```yaml
# kb/people/<slug>.md frontmatter additions
phone: "+1 415 555 0123"
address: "500 Kearny St, San Francisco, CA"
title: "VP Engineering"
```

**Image signatures.** Many professional signatures are rendered as an
image (PNG/JPG attachment inline). To transcribe them, use an available
OCR/vision tool from the inventory — `gemini` with `--image`, or any
multimodal model available to the agent. Feed the image with the prompt:
*"Transcribe this email signature verbatim. Return fields: name, title,
company, phone, email, address, socials (twitter/linkedin/github URLs)."*

Write the transcribed fields to the frontmatter. If the OCR is unclear
for a given field, leave it blank and log a gap.

## Never do these

- Do not infer facts about the person from their name, photo, or perceived
  demographics. Stick to verifiable signals.
- Do not merge two people with the same name without confirming (ask the user
  if ambiguous — two "John Smith"s should not collapse).
- Do not query tools that aren't in `ready` inventory.
- Do not cache LeadClaw responses on disk outside the KB raw/ (they have PII
  and should live under the controlled KB layout, never `/tmp`).
- Do not paste email body text verbatim into the KB — summarise. Phone
  numbers, addresses, titles go into frontmatter; conversation topics go
  into `## Prior conversations` as one-liners.
- Do not treat a private/school/isp email domain as a company indicator.
