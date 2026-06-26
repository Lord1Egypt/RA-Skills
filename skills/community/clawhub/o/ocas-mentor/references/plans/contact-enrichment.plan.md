---
plan_id: contact-enrichment
name: Contact Enrichment
version: 1.0.0
description: Enriches a Weave contact by scanning all Gmail history for that person, then running Scout OSINT research, then Sift open-web search -- writing high-confidence facts back to Weave at each step.
parameters:
  contact_id:
    type: contact_id
    required: false
    description: Weave person_id to enrich. If omitted, a random contact is selected.
  confidence_threshold:
    type: number
    required: false
    default: 0.75
    description: Minimum confidence score (0.0-1.0) required before writing a fact to Weave. Applied in Scout and Sift steps.
  gmail_max_messages:
    type: number
    required: false
    default: 500
    description: Maximum number of individual Gmail messages to review per query. Increase for contacts with very high email volume.
steps:
  - id: select-contact
    name: Select Contact
    skill: ocas-weave
    command: weave.query
    on_failure: abort
  - id: gmail-scan
    name: Gmail Scan and Extraction
    skill: gog
    command: gmail-messages-search
    on_failure: skip
  - id: scout-research
    name: Scout OSINT Research
    skill: ocas-scout
    command: scout.research
    on_failure: skip
  - id: sift-research
    name: Sift Open-Web Research
    skill: ocas-sift
    command: sift.research
    on_failure: skip
---

# Contact Enrichment

## Purpose

This plan systematically enriches a single Weave contact record using three independent signal sources: the user's own Gmail history (highest confidence -- first-party signals), Scout OSINT from public records (high confidence -- verified public data), and Sift open-web search (moderate confidence -- filtered by threshold).

Each step adds to Weave with full provenance. Steps 2-4 are independently marked `on_failure: skip` so a Gmail outage or absent OSINT data does not abort the whole run. The contact record grows richer across all three passes in a single plan run.

Run this plan periodically (e.g., weekly via cron) against random contacts to maintain a well-enriched social graph over time.

---

## Step 1: select-contact

**Skill:** ocas-weave
**Command:** weave.query

**Inputs:**
- `mode`: `"lookup"` if `{{params.contact_id}}` is non-null, else `"random"`
- `person_id`: `{{params.contact_id}}` (null triggers random selection)

Random selection query (use when contact_id is null):
```cypher
MATCH (p:Person)
WHERE p.email IS NOT NULL OR p.name IS NOT NULL
RETURN p ORDER BY rand() LIMIT 1
```

**Outputs:**
- `contact`: full Person node including `person_id`, `name`, `email`, `phone`, `location`, `employer`, `aliases`, `record_time`, and all attached Preference and Knows edges
- `existing_fact_count`: total number of facts (preferences + relationships) already in the record

**On failure:** abort
**Notes:** If no Person nodes exist in Weave, abort with message "Weave has no contacts -- run weave.upsert.person or weave.sync.google-contacts first." Do not proceed with an empty result.

---

## Step 2: gmail-scan

**Skill:** gog (Gmail via `gog gmail messages search`)
**Command:** gmail-messages-search

**Inputs:**

Build a query list from the contact record. Run each query separately and collect all results, deduplicating by message ID:

| Query | Purpose |
|---|---|
| `from:{{steps.select-contact.contact.email}}` | Emails the contact sent to you |
| `to:{{steps.select-contact.contact.email}}` | Emails you sent to the contact |
| `"{{steps.select-contact.contact.name}}"` | Name mentions in any thread |
| For each alias in `contact.aliases`: `"{{alias}}"` | Catch informal name variants |

Shell pattern for each query:
```bash
gog gmail messages search "{query}" --max {{params.gmail_max_messages}} --account $GOG_ACCOUNT --json
```

**Review ALL returned messages -- not a sample.** This is the only step with direct access to first-party signals. Skimming degrades enrichment quality significantly.

**Extraction targets** (look for these in every message body and signature):

- **Relationships**: any mention of family members (spouse, children, parents, siblings), close colleagues, or named connections ("my partner Alex", "my daughter Emma")
- **Life events**: birthdays, anniversaries, births, deaths, job changes, moves, graduations, health events -- note the date if present
- **Alternative contact methods**: phone numbers in signatures, secondary email addresses, social handles
- **Current employer and role**: from email signatures (employer name, title, department)
- **Location**: city or region from signature, out-of-office messages, or contextual mentions
- **Topics of interest**: recurring subjects, hobbies, professional interests that appear across multiple threads
- **Preferred name**: if they sign emails with a different name than their display name, record as alias

**Write-back rules:**
- Source type: `inferred` for anything extracted from email content; `user-stated` only if the contact explicitly stated a fact about themselves in first person
- `source_ref`: Gmail message ID (format: `gmail:{message_id}`)
- `record_time`: current timestamp
- `confidence`: `0.9` for facts from signatures (structured, stable); `0.75` for facts from body text (contextual, may be stale)
- Do not write facts with confidence below 0.70
- Do not write relationship edges without confirming both Person nodes exist in Weave first. If a mentioned person does not exist, create a minimal Person stub (`name` only) via `weave.upsert.person` before adding the `Knows` edge
- Use `weave.upsert.preference` for preferences and life events; use `weave.upsert.person` for updates to the contact's own core fields (employer, location, phone, aliases); use `weave.upsert.relationship` for `Knows` edges

**Outputs:**
- `enriched_contact`: updated Person node after all writes (re-query Weave for the current record)
- `facts_added`: count of new facts written
- `aliases_discovered`: list of any new name variants found (used by Scout and Sift for better search queries)
- `employer`: most recent employer string found (passed to Scout/Sift for identity confirmation)
- `location`: most recent location string found (passed to Scout/Sift for identity confirmation)

**On failure:** skip
**Notes:** If `gog` is not installed or not authenticated, skip this step and log the reason. The plan continues with Scout and Sift using only the original Weave record for identity context.

---

## Step 3: scout-research

**Skill:** ocas-scout
**Command:** scout.research

**Inputs:**

Build the research subject from the enriched contact profile:

```
Subject name: {{steps.select-contact.contact.name}}
Known aliases: {{steps.gmail-scan.aliases_discovered}} (plus existing aliases from contact record)
Email: {{steps.select-contact.contact.email}}
Employer: {{steps.gmail-scan.employer}} or {{steps.select-contact.contact.employer}}
Location: {{steps.gmail-scan.location}} or {{steps.select-contact.contact.location}}
Phone: {{steps.select-contact.contact.phone}}

Research goal: Find high-confidence public facts to enrich this person's Weave contact record.
Permitted sources: Tier 1 (public web) and Tier 2 (rate-limited registries) only.
Tier 3 (paid OSINT): do not use without explicit user permission.
```

**Identity heuristics -- these are mandatory for this step:**
- Accept a result as being about this person only if it matches: name + at least one of (email | employer | location | phone)
- Common name guard: if the name is a common first+last combination (e.g., "John Smith"), require name + two independent secondary facts before accepting any result
- If identity cannot be confirmed with high confidence, do not write any facts from that result -- log the ambiguity and continue

**What to extract and write to Weave:**
- Professional bio (current role, employer, notable work)
- Social profiles (LinkedIn URL, Twitter/X handle, personal website) -- write as preferences with `source_type: imported`
- Public location (city, state) if more precise than what is in Weave
- Areas of expertise or professional interests
- Any publicly listed contact methods not already in Weave

**Write-back rules:**
- `source_type`: `imported` for data from public directories; `inferred` for facts extracted from bio text
- `source_ref`: URL of the source page with retrieval timestamp
- `confidence`: only write facts Scout rates as high confidence (>= `{{params.confidence_threshold}}`)
- Do not overwrite existing facts with lower-confidence data -- add as additional provenance instead

**Outputs:**
- `osint_facts_added`: count of high-confidence facts written to Weave
- `identity_confirmed`: `true` if Scout confirmed this is the correct person; `false` if identity was ambiguous
- `scout_brief_path`: path to Scout's research brief artifact (for auditability)

**On failure:** skip
**Notes:** If `identity_confirmed` is false, log the reason (common name, insufficient secondary facts, conflicting signals) and skip writing anything. Do not write speculative matches.

---

## Step 4: sift-research

**Skill:** ocas-sift
**Command:** sift.research

**Inputs:**

Build a set of research queries from the fully enriched contact profile (using outputs from all prior steps):

```
Primary query: "{{steps.select-contact.contact.name}}"
Supplementary context:
  - employer: {{steps.gmail-scan.employer}} or {{steps.select-contact.contact.employer}}
  - location: {{steps.gmail-scan.location}} or {{steps.select-contact.contact.location}}
  - email: {{steps.select-contact.contact.email}}
  - social handles: any discovered in prior steps

Research goal: Find additional publicly available information about this person to enrich their Weave contact record.
Confidence threshold: {{params.confidence_threshold}}
```

Run Sift in `deep research` mode. Construct query permutations including:
- `"{{name}}" {{location}}` -- geographic disambiguation
- `"{{name}}" {{employer}}` -- professional disambiguation
- `"{{name}}" site:linkedin.com` -- if LinkedIn profile not already in Weave
- `"{{name}}" {{known_social_handle}}` -- if social handles found in prior steps
- `"{{name}}" {{email}}` -- email-specific search

**Identity heuristics -- mandatory:**
- Apply the same name + secondary fact confirmation rule as Step 3
- Treat Sift results as lower confidence than Scout by default -- apply an additional -0.05 penalty to any confidence score Sift reports before comparing to `{{params.confidence_threshold}}`
- Prefer corroborated facts (found in 2+ sources) over single-source facts

**Write-back rules:**
- Only write facts that pass the adjusted confidence threshold
- `source_type`: `imported`
- `source_ref`: source URL with retrieval timestamp
- Do not duplicate facts already written by Steps 2 or 3 -- check existing Weave record before writing

**Outputs:**
- `web_facts_added`: count of facts written to Weave
- `enrichment_summary`: human-readable summary of what was added across all four steps (total facts added, categories covered, confidence distribution)

**On failure:** skip

**Notes:** Sift is the lowest-confidence source in this plan. If Steps 2 and 3 were both skipped, be more conservative -- require corroboration from 2+ Sift sources before writing anything. The goal is durable, accurate enrichment, not maximizing fact count.

---

## Plan Completion

After Step 4, log a final summary DecisionRecord to `decisions.jsonl` containing:
- `plan_run_id`
- `contact enriched`: `{{steps.select-contact.contact.name}}` (`{{steps.select-contact.contact.person_id}}`)
- `steps completed`: which steps ran vs. were skipped
- `total facts added`: sum across all steps
- `identity confirmed by Scout`: value of `{{steps.scout-research.identity_confirmed}}`

Write a journal entry covering the full plan run as an Action Journal.

---

## Scheduling

To enrich a random contact daily:

```bash
openclaw cron add --name mentor:contact-enrich \
  --schedule "0 3 * * *" \
  --command "mentor.plan.run contact-enrichment" \
  --sessionTarget isolated --lightContext true --wakeMode next-heartbeat \
  --timezone America/Los_Angeles
```

To enrich a specific contact on demand:

```
mentor.plan.run contact-enrichment --arg contact_id=person_abc123
```

To raise the confidence bar for a more conservative run:

```
mentor.plan.run contact-enrichment --arg confidence_threshold=0.85
```
