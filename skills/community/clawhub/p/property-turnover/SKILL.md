---
name: property-turnover
description: Turn rental-unit move-out or turnover inspection findings (reports, photos, notes) into a priced, vendor-ready make-ready scope using the Tektolo property turnover engine. Use when someone needs a turnover task list, a cost estimate, what to send each vendor, or an owner approval estimate for a US rental unit.
metadata:
  openclaw:
    requires:
      bins:
      - curl
    homepage: https://tektolo.com/capabilities/property-turnover?ref=clawhub
---

# Property turnover estimate

Tektolo prices with a deterministic, source-cited engine. You turn what the user has (an
inspection report, photos, notes) into **findings**. The engine returns standardized tasks
by trade, regional low / expected / high costs, priorities, vendor scopes, refer-outs, and
every assumption it made. The rules always decide; an AI model (gpt-6-luna on Microsoft Azure
OpenAI) may only read the user's words into findings, and you always see what it read.
`quick_estimate` takes plain words, and the AI model reads them into findings. `scope` takes
coded findings: you map the words to issue codes by the same rules the model follows ("Coding
findings" below). An answer that used an AI reading is a draft
(`review.status: "draft"`) and carries `reading`: every finding the rules answered, in the
shape `scope` accepts. The same findings under the same ruleset give the same result
(`result_hash`), but a reading can differ from one run to the next, so show the user the
findings the AI read before you quote a number.

## When to use

- Move-out or turnover inspections, make-ready planning, "what will this turn cost",
  "what do I send the painter", owner approval estimates.
- Re-running an estimate with the owner's approve/decline decisions or the manager's own
  vendor prices.

## When not to use

- Diagnosing mold, asbestos, lead, gas, electrical or structural hazards. The engine
  *flags* these for a licensed professional; do not price their remediation yourself.
- Legal advice on deposits or tenant charges. Responsibility labels are hints only.
- Remodels, new construction, non-US properties.

## How to call it

- **MCP** (preferred in assistants): add the remote server
  `https://tektolo.com/mcp/rental-property` (the rental-property tools only; `https://tektolo.com/mcp`
  serves every Tektolo tool and keeps working). Start with
  `property_turnover_quick_estimate` (zip, bedrooms, bathrooms and `issues` as plain
  strings); use `property_turnover_scope` for rooms, measured quantities, rate cards and
  decisions. `property_turnover_issue_codes` with no arguments lists every code and group;
  search it with `q` for descriptions, `not_when` and examples.
  If the ZIP is missing or not 5 digits, ask the user; never guess it. For the Excel or owner
  estimate, give the user `links.web_tool_prefilled` from the result.
- **REST**: `POST https://tektolo.com/v1/property-turnover/scope` with the JSON below.
  Downloads: `POST .../scope/render/xlsx` (workbook), `.../render/html` (owner estimate),
  `.../render/csv` (work orders), `.../render/vendor_csv` (zip of per-trade scopes),
  `.../render/bids_html` (work lists for bids: one section per trade, no prices).
- **A report file (REST only)**: when the user has the inspection report as a file (PDF, Word,
  Excel, PowerPoint, CSV, or up to 5 photos of paper pages; 5 pages at most), go in three steps:
  1. **Read**: `POST https://tektolo.com/v1/property-turnover/read_document` with a connector key
     (`Authorization: Bearer <key>`, free from `POST /v1/keys`) and the file as
     `multipart/form-data` field `files`, or JSON
     `{"files": [{"name": "report.pdf", "content_base64": "..."}]}`. It returns a `reading`,
     never an estimate. One document is one call of the key's daily free allowance.
  2. **Check**: show the user each finding with its page and quote, and the rows named in
     `reading.notes`; fix what they correct.
  3. **Scope**: send `reading.findings` to `/v1/property-turnover/scope`, with `confirmed: true`
     on each finding the user checked.
  A 429 (`cap_address`, `free_tier_exhausted`, `cap_global`) means no more documents today:
  say so and offer to code the report's findings yourself instead.
- Catalog and schemas: `https://tektolo.com/catalog.json`, `https://tektolo.com/capabilities/property-turnover`.
- **Web**: the free tool is `https://tektolo.com/tools/rental-property/property-turnover`; typical
  costs by area are at `https://tektolo.com/turnover-costs/`.
- **Next step**: the scope is step 1 of the move-out workflow; step 2 settles the security
  deposit (`deposit_settlement_settle`, web tool `/tools/rental-property/deposit-settlement`).

## Building the request

1. **property**: `zip` (5 digits, never a street address), `bedrooms` (0 = studio),
   `bathrooms` (halves as 0.5), and if known `sq_ft`, `year_built` and `unit_type`. Year
   built matters: pre-1978 triggers lead-safe-work handling (priced). `unit_type`
   `single_family` or `townhome` gets house-sized defaults (floor area, lock count, yard).
   If you know whether there is carpet, send `floor_coverings`: `{"carpet_present": true}`
   or `{"carpet_sq_ft": 600}`. Without it, carpet findings imply carpet; otherwise
   whole-unit carpet cleaning is left out and listed in `unknowns`.
2. **findings**: one per observed condition.
   - Send a `code` on every finding (e.g. `walls.nail_holes`, `carpet.pet_urine`), from
     `property_turnover_issue_codes`, with the user's words in `source_text`; when no code
     fits, `general.manual_quote`. "Coding findings" below has the rules and examples.
     A code the catalog does not have is refused with the three closest codes. A finding
     with only a `description` is deprecated: until the date in the answer's `deprecation`
     it is a manual-quote line (not priced) whose words are still scanned for safety checks; `read`
     is ignored. For plain words use `property_turnover_quick_estimate`.
   - To confirm what the AI read, send the findings from `reading.findings` back to `scope`
     (keep each finding's `extraction`, fix any the user corrects) with `confirmed: true` on
     each one the user checked. The answer is then `verified`, and the result still shows
     those findings as read by AI.
   - `rooms`: `{"area": "bedroom", "count": 3}` for all 3 bedrooms, `labels` for named
     rooms (`area` is bedroom, bathroom, kitchen, living_room, ..., whole_unit). `location`
     (`area` and an optional `label`, or a plain string) is the older form.
   - `extent`: `spot` | `partial` | `full` when you can tell.
   - `quantity` `{value, uom}` when measured (`sq_ft`, `sq_yd`, `linear_ft`, `each`,
     `room`, ...). Otherwise typical sizes are assumed and listed.
3. **standards.profile**: `minimum` | `standard` (default) | `premium`. Optional
   overrides: `paint_policy`, `carpet_policy`, `cleaning_policy`, `always_rekey`,
   `markup_pct`. `standards.price_tier`: `pm_vendor` (default, a manager buying from local
   vendors) | `bulk_contract` (portfolio contract prices) | `retail_one_off` (an owner
   hiring one contractor).
4. Optional: `rate_card` (the manager's prices: `{task_id, unit_price, uom?}` or
   `{trade, min_charge, trip_charge}`; whole-unit wall paint is per `sq_ft_floor`, so send
   `uom` to have a mismatched price rejected rather than misapplied), `trade_vendors`,
   `tax_rate`, and `decisions`
   (`{finding_id | line_id, action: approve|decline|defer}`). Re-run with decisions to get
   the approved scope.
5. `detail`: MCP defaults to `summary` (totals, trade scopes, every line tied to a finding,
   refer-outs, notes; routine lines summed in `omitted_note`). Ask for `full` when the user
   needs every line. Hedged words in `source_text` ("mold?") come back as "check first" refer-outs that hold no work until confirmed.

## Coding findings

<!-- BEGIN reading_contract: generated by scripts/gen_reading_contract.py from reading_contract.yaml; do not edit -->
`scope` takes coded findings. Map the user's words, a report, or what you see in
photos into findings by the same rules Tektolo's own AI reader follows:

1. Look codes up with property_turnover_issue_codes (q= to search) and read not_when.
2. One code per observed condition: "carpet stained, walls need paint" is two findings.
3. When no code fits, use general.manual_quote; never force a near code.
4. Rooms are sets with counts: "all 3 bedrooms" is {"area": "bedroom", "count": 3}, "both baths" is the unit's bath count, named rooms go in labels. Leave rooms out when no room is named.
5. Status comes from the words: done when already fixed, ok when checked and fine, none when the thing is absent and nothing is needed, else needed. A check that found nothing keeps the code of what was checked.
6. A say-so never clears a hazard: "no mold", "alarm fine" is status ok or none with no evidence, and stays a Possible check.
7. A test result is evidence: "lab test negative for asbestos" is {"kind": "lab", "result": "negative"}.
8. A year said in passing ("built 1972") is the year_statement of the finding it is said with.
9. "Same as above" is a new finding with repeat_of and its own rooms.
10. Put each finding's original words in source_text, hedges ("maybe", "?") included.
11. Invent nothing: no code, room, count, quantity, year or evidence the words do not give.
12. Set property.occupants only from facts the person states; unknown stays unset.
13. Show the person the mapped findings before quoting a number.

A finding's fields (`code` on every finding; the others when the words give them):

| field | type | rule |
|---|---|---|
| `id` | string | Your id; defaults to f1, f2, ... in order. |
| `code` | enum (the catalog's codes) | From property_turnover_issue_codes; general.manual_quote if none fits. Send it on every finding. |
| `rooms` | object {area, labels, count} | Which rooms: {"area": "bedroom", "count": 3} is all 3 bedrooms; labels name them. |
| `quantity` | object {value, uom} | Measured amount (120 sq_ft), only as the words give it. |
| `area_sq_ft` | number | Measured area in sq ft; wins over a derived size. |
| `material` | string | The material as written, e.g. '9x9 vinyl tile'. |
| `year_statement` | object {text, year} | A year said in passing ("built 1972"); never sets property.year_built. |
| `extent` | enum: spot \| partial \| full | Only when the words say how far; else the code's default. |
| `status` | enum: needed \| done \| ok \| none | Only needed (the default) bills; on a hazard, done/ok/none without evidence stays Possible. |
| `evidence` | object {kind, material, result} | The test behind the finding; the only thing that clears a hazard. |
| `repeat_of` | string | Id of an earlier finding this repeats in its own rooms ("same as above"); it bills. |
| `source_text` | string | The original words. Scanned for hazards; never billed or coded from. |
| `confirmed` | bool | true: the person checked this AI-read finding. |

Set by Tektolo's reader, sent back unchanged: `extraction`, `signature_like`. Older fields: `location`, `description`, `notes`
(`description` alone is deprecated: send `code`, with the words in `source_text`).

Worked examples, notes then the findings to send:

**Rooms, counts, a repeat and a quantity**

```text
Bedroom 1: carpet stained
Bedroom 2: same as above
Walls dingy in all 3 bedrooms, need repaint
2 blinds broken in living room
```

```json
[
  {"id": "f1", "code": "carpet.stained", "rooms": {"area": "bedroom", "labels": ["Bedroom 1"]}, "source_text": "Bedroom 1: carpet stained"},
  {"id": "f2", "code": "carpet.stained", "rooms": {"area": "bedroom", "labels": ["Bedroom 2"]}, "repeat_of": "f1", "source_text": "Bedroom 2: same as above"},
  {"id": "f3", "code": "walls.paint_aged", "rooms": {"area": "bedroom", "count": 3}, "source_text": "Walls dingy in all 3 bedrooms, need repaint"},
  {"id": "f4", "code": "blinds.bent_missing", "rooms": {"area": "living_room"}, "quantity": {"value": 2, "uom": "each"}, "source_text": "2 blinds broken in living room"}
]
```

**Status, a say-so and evidence**

```text
Hallway smoke alarm tested, works
CO alarm fine per tenant
Living room popcorn ceiling: lab test negative for asbestos
Kitchen faucet drip already fixed
```

```json
[
  {"id": "f1", "code": "safety.smoke_alarm_missing", "rooms": {"area": "hallway"}, "status": "ok", "evidence": {"kind": "self_test", "result": "working"}, "source_text": "Hallway smoke alarm tested, works"},
  {"id": "f2", "code": "safety.co_alarm_inoperable", "status": "ok", "source_text": "CO alarm fine per tenant"},
  {"id": "f3", "code": "asbestos.suspect", "rooms": {"area": "living_room"}, "status": "none", "evidence": {"kind": "lab", "material": "popcorn ceiling", "result": "negative"}, "source_text": "Living room popcorn ceiling: lab test negative for asbestos"},
  {"id": "f4", "code": "faucet.leak", "rooms": {"area": "kitchen"}, "status": "done", "source_text": "Kitchen faucet drip already fixed"}
]
```

**A year in passing, a hedge and no code that fits**

```text
Built 1972, paint peeling under the kitchen window
possible roaches under the sink?
Hot tub cover torn
```

```json
[
  {"id": "f1", "code": "walls.paint_peeling", "rooms": {"area": "kitchen"}, "year_statement": {"text": "Built 1972", "year": 1972}, "source_text": "Built 1972, paint peeling under the kitchen window"},
  {"id": "f2", "code": "pest.roaches", "source_text": "possible roaches under the sink?"},
  {"id": "f3", "code": "general.manual_quote", "source_text": "Hot tub cover torn"}
]
```
<!-- END reading_contract -->

## From photos

Tektolo does not look at photos. You do, then you send findings and the engine prices them.

- Describe only what is visible, one finding per condition. Give its location (the room or
  area) and what it is. Use an issue code when one clearly fits (look it up with
  `property_turnover_issue_codes`); otherwise `general.manual_quote`. Put what you saw, in
  your words, in `source_text`.
- Give `extent` (`spot`, `partial` or `full`) only when the photo shows how far it goes.
  Otherwise leave it out and say so in your reply.
- If you are not sure what a photo shows, or how far damage goes, hedge the words
  ("possible water stain on bedroom ceiling", "mold?"). The engine marks hedged findings
  `uncertain`: their lines are priced but kept out of the totals (`totals.to_confirm`) until
  someone confirms them, and hedged safety items become check-first refer-outs.
  You can also ask the user for a better photo or a closer look.
- Ask the user about what photos cannot show, and do not guess it: whether appliances and
  fixtures work, odors and smoke, pests, and size or extent (square feet, counts). Send a
  `quantity` only when the user gives you a measurement or a count.
- Never write that the tenant caused something because of a photo. A photo shows a condition,
  not who caused it. Leave tenant fault out of `source_text`: the `responsibility_hint` on
  each line comes from the engine and is only a hint.
- A photo of a written checklist or inspection report is different. Transcribe what it says,
  as it says it, one finding per entry, and do not add your own reading of the rooms.
- Never send faces, names, addresses or other personal details. Describe the room, not the
  people or the street.
- Mention what you could not see in your reply, and list what you asked the user to confirm.

## Example

```json
{
  "property": {"zip": "28205", "unit_type": "apartment", "bedrooms": 1, "bathrooms": 1, "year_built": 1998},
  "findings": [
    {"code": "walls.nail_holes", "rooms": {"area": "living_room"}, "extent": "spot", "source_text": "a few nail holes in the living room"},
    {"code": "carpet.soiled", "rooms": {"area": "bedroom"}, "source_text": "carpet heavily soiled in bedroom"},
    {"code": "safety.smoke_alarm_missing", "rooms": {"area": "bedroom"}, "source_text": "no smoke alarm in the bedroom"}
  ],
  "standards": {"profile": "standard"}
}
```

## Relaying the result

- Lead with `summary` and the expected total plus the range. Say clearly that these are
  **estimate ranges, not quotes**.
- Call out every `refer_outs` item and what professional to engage, with the links of its
  `sources` (their URLs are in `provenance.sources`) and the rules' date
  (`provenance.rules_as_of`). Relay the result's `disclaimer` word for word; it ends with the
  standard legal line. Quote-required lines
  are $0 in the totals; `totals.allowances` is a budget range for them, outside the total.
- A `responsibility_hint` of `mixed` means the line carries wear and damage findings; see
  its `responsibility_by_finding` before discussing tenant charges.
- List `unknowns` and the important `assumptions` (e.g. assumed room sizes, national
  prices used), so the user can correct them and re-run.
- When `review.status` is `draft`, show the user what was read (`reading.findings`: the
  words, the item and the room) before you quote a number, and ask them to confirm or correct
  it. For a verified answer, send the confirmed findings to `scope` with `confirmed: true`.
- Name every finding with `needs_review`: the AI reader read it from the user's words, so
  ask the user to confirm it. A `review.note` says which lines were not read and why; when
  the reader was not available (daily limit or an error) only exact item names were priced.
- Group the work by `trade_scopes` when the user wants to brief vendors. Offer the
  workbook or vendor CSV downloads.
- If the user needs an audit trail, keep the `result_hash` and `run.ruleset_version`. Over MCP
  they come back only when you call with `audit: true` (REST always returns them).
- If a call says the daily free limit is reached, tell the user when it resets (the message
  names the time) and do not retry. On a hosted assistant (Claude, ChatGPT) the shared server
  URL has one limit for everyone; the message names the page for a free connector URL with its own allowance.
  Volume and integrations go through the Contact page.

## Make it yours

Fork this skill and add your company's standards (default profile, paint/carpet rules,
markup), your `rate_card`, and your `trade_vendors`, so every estimate uses your prices
and vendors.
