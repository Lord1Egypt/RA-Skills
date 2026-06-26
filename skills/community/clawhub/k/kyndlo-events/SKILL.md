---
name: kyndlo-events
description: "WORKFLOW-DRIVEN event creation and validation from Kyndlo campaign tasks. When invoked, the agent MUST follow the mandatory step-by-step onboarding flow below — verify token, show campaigns, ask city, ask county, ask batch size, fetch rules — before creating any events. For validation, follow the Event Validation Workflow. Do NOT ask generic questions. Do NOT improvise. Follow the steps exactly."
version: 3.5.0
metadata:
  openclaw:
    requires:
      env:
        - KYNDLO_API_TOKEN
      bins:
        - node
        - gokyn
    primaryEnv: KYNDLO_API_TOKEN
    install:
      - kind: npm
        package: gokyn
        bins: [gokyn]
        label: npm install -g gokyn
    emoji: "🎉"
    os: [darwin, linux]
    homepage: https://github.com/kyndlo/gokyn-cli
---

# kyndlo-events — Kyndlo Event Management

**CRITICAL: This skill has MANDATORY step-by-step workflows for both event creation and event validation. You MUST follow the exact steps in order. Do NOT skip steps. Do NOT ask your own questions. Do NOT improvise. The workflow tells you exactly what to run and what to ask at each step.**

## STOP — Read This First

When this skill is invoked (user says anything like "create events", "kyndlo-events", "generate events", etc.):

**If the user says "validate events", "check events", "review events", or "validation"** — skip directly to the **Event Validation Workflow** section below.

For event creation:

1. **Do NOT** ask the user for city, date range, event style, theme, or any other freeform questions
2. **Do NOT** try to gather requirements conversationally — the workflow below handles that
3. **DO** immediately start at Step 1 below and follow every step in order
4. **DO** run the CLI commands shown — they provide the data you need
5. **DO** wait for the user's response where indicated before moving to the next step
6. **DO** always check for existing events before creating — duplicates waste resources

Events are created from **campaign tasks** stored in the Kyndlo database, not from user-provided descriptions. The system tells you what events to create. Your job is to follow the workflow.

## Setup

```bash
npm install -g gokyn
export KYNDLO_API_TOKEN="kyndlo_..."
export GOOGLE_PLACES_API_KEY="..."   # Required for venue discovery via goplaces
```

All gokyn commands accept `--token <token>` if the env var is not set.
Add `--json` to any command for machine-readable output.
`goplaces` is used for venue discovery (Google Places API). It must be installed and configured separately.

---

## Step 1: Verify token

**Action:** Run this command immediately — do not ask the user anything first.

```bash
gokyn whoami --json
```

Confirm the token is valid. If it fails, help the user set `KYNDLO_API_TOKEN`.

## Step 2: Show campaigns and ask the user to pick one

**Action:** Run this command:

```bash
gokyn task campaigns
```

**Then say to the user:**
> "Here are the available campaigns: [show the list with name, state, progress, pending tasks]. Which campaign would you like to work on?"

**STOP and wait for the user's reply.** Extract the campaign name and state from their choice.

## Step 3: Show cities and ask which to prioritize

**Action:** Run this command using the state from the campaign they chose:

```bash
gokyn task cities --state "<state>"
```

**Then say to the user:**
> "Here are the cities in [state]: [show city list with populations]. Which city would you like to prioritize? Say a city name, or 'any' to work through all cities."

**STOP and wait for the user's reply.** Handle:
- **"any"** — Rotate through cities automatically. Start with the first city that has pending tasks.
- **Specific city** — Lock to that city. Proceed to Step 4.

## Step 4: Ask about county preference

**Say to the user:**
> "Would you like to focus on a specific county, or work through all of them? (By default, I'll focus on major city counties and skip rural counties. Say 'include rural' if you want those too.)"

**STOP and wait for the user's reply.** Handle:
- **No preference / default** — Ignore rural counties. Never use `--city "Rural"`. Skip the "Rural" entry when rotating. This is the default.
- **"include rural"** / **"all including rural"** — Include rural counties. No county filter.
- **Specific county** — Use `--county <county>` filter.
- **"all"** (without mentioning rural) — Ignore rural counties (the default).

## Step 5: Ask batch size

**Say to the user:**
> "How many events should I create before pausing to report results? (e.g. 5, 10, 20)"

**STOP and wait for the user's reply.** Store this as the batch size.

## Step 6: Fetch event creation rules (MANDATORY — do not skip)

**Action:** Run this command:

```bash
gokyn task rules
```

Read the **full** output and internalize every rule. These rules come from the Kyndlo admin dashboard and govern venue selection, descriptions, formatting, images, and quality. **You must follow them strictly for every event.**

## Step 7: Confirm and begin

**Say to the user:**
> "Ready to start. Here's your configuration:
> - Campaign: [name]
> - State: [state]
> - City: [specific city / rotating through all]
> - County filter: [ignore rural (default) / include rural / specific county]
> - Batch size: [N] events per batch
> - Rules: Loaded
>
> Shall I begin?"

**STOP and wait for confirmation.** Only proceed to the Autonomous Loop after the user says yes.

---

## Category Name Mapping

Task `activityCategory` values sometimes differ from activity titles in the database. Use this table when searching for the activity ID:

| Task activityCategory | Search Term for `gokyn activity list --search` |
|---|---|
| Specialty Niche Museums | Specialty & Niche Museums |
| Yoga Classes | Wellness centers |
| Restaurant/Cafes with Animal Encounters | Coffee with animal encounters |
| Community Theaters | Theater lounges |
| Craft Cafes | Craft cafés |
| Beach/Boardwalks | Beach Boardwalks |
| Food Trucks | Food truck parks |
| Planetariums | Planetarium |

If the task category is not in this table, use it as-is for the search.

---

## Day-of-Week Reference

When setting `--recurrence-days`, use these day numbers:

| Day | Number |
|-----|--------|
| Sunday | 0 |
| Monday | 1 |
| Tuesday | 2 |
| Wednesday | 3 |
| Thursday | 4 |
| Friday | 5 |
| Saturday | 6 |

Include a day ONLY if the venue is open that day. Omit closed days entirely.

---

## State Timezone Reference

| State | Timezone |
|-------|----------|
| Colorado | America/Denver |
| Florida | America/New_York |
| New York | America/New_York |

---

## The Autonomous Loop

Process tasks in batches. Each batch creates up to **N** events (the batch size from onboarding), then pauses to report results and ask the user whether to continue.

**Important:** If the loop exits early for any reason, run the Cleanup step to release any uncompleted tasks.

### Before each batch: Refresh rules

At the start of **every** batch (including the first), fetch the latest rules:

```bash
gokyn task rules
```

Re-read and internalize. Rules may have been updated by the Kyndlo admin between batches.

### City rotation (when city = "any")

Track the current city. When `task next` returns `"count": 0` for the current city:

1. Get the city list: `gokyn task cities --state "<state>" --json`
2. For each city (in order), check for pending tasks: `gokyn task context --campaign <campaign> --city "<city>" --json`
3. Skip "Rural" if the user said "ignore rural counties"
4. Use the first city with remaining pending tasks
5. If no cities have pending tasks, stop the loop

### Rural filtering

When the user chose "ignore rural counties":
- Never pass `--city "Rural"` to any command
- When rotating through cities, skip the "Rural" entry
- If a task is returned for a rural county (shouldn't happen with city filter), release it and continue

### Step 1: Claim a task

```bash
gokyn task next --campaign <campaign> --city <city> --assign --name "<agent-name>" --json
```

Apply filters based on onboarding preferences:
- If a specific county was chosen: add `--county <county>`
- Use the agent name only for `--name` (e.g. `Sugar`). Do NOT pass `--priority` — the server returns tasks in priority order automatically.

If `"count": 0`:
- If city = "any": rotate to the next city (see City Rotation above)
- If specific city: stop the loop
- If the response includes a `"diagnostic"` field, report it to the user

Extract from `tasks[0]`: `_id` (taskId), `county`, `activityCategory`, `cluster`, `state`.

### Step 2: Map the category

Check the Category Name Mapping table above. If the `activityCategory` matches a left-column entry, use the corresponding right-column search term. Otherwise use the category as-is.

### Step 3: Find the activity ID

```bash
gokyn activity list --search "<mapped-category>" --json
```

Extract the activity `_id` from the first matching result. If no results, try shorter/partial search terms. If still no match, skip the task with reason "Activity not found for category: \<category\>".

### Step 4: Research a venue

Find a real venue matching the task's `activityCategory` in `county`, `state`. Use **goplaces** (Google Places API) as the primary discovery tool.

#### 4a. Search for candidates

```bash
goplaces search "<category> in <county> County, <state>" --json --limit 5 --region US
```

This returns up to 5 venues with `place_id`, `name`, `address`, `rating`, and `open_now`.

#### 4b. Get full details for the best candidate

```bash
goplaces details <place_id> --json
```

Extract from the response:
- **name** — venue display name
- **address** — full street address (verify it's in the correct county!)
- **location.lat** / **location.lng** — GPS coordinates
- **regular_opening_hours.weekday_descriptions** — operating hours per day
- **website** — venue website (used as `--booking-url`)
- **price_level** — price indicator (0=free)

#### 4c. Validation gates

Before using a venue, verify ALL of these:

1. **County match** — The address must be in the task's county. If the address says a different city/county, reject it.
2. **Hours exist** — `regular_opening_hours` must be present. If `None` or missing, reject the venue.
3. **Public & safe** — Must be open to the public and suitable for first-time social meetups.

Convert hours to open day numbers (0=Sun through 6=Sat). Include a day ONLY if the venue is open that day.

#### 4d. Fallback

If goplaces returns no results or all candidates fail validation:
- Try broader search terms (e.g. shorter category name, nearby city name)
- Try web search as a last resort to find hours or verify county
- If still no qualifying venue after 5 candidates, skip the task

**Collect for the chosen venue:**
- **name**, **address**, **lat**, **lng**, **open days** (as numbers 0-6), **website URL**, **price** (default 0)
- **Venue atmosphere details** (for image generation prompt in Step 7): interior/exterior style, lighting, mood, notable features

### Step 5: Check for duplicate events (MANDATORY — do not skip)

Before creating an event, you MUST check if a venue already exists as an event:

```bash
gokyn event list --search "<venue name>" --json
```

**Duplicate detection rules:**
- If any result has the **same title** (case-insensitive) AND is in the **same county** → this is a duplicate. Skip this venue and try the next candidate.
- If any result has a **similar title** (substring match) AND the **same address** → this is a duplicate. Skip this venue and try the next candidate.
- If **all** venue candidates for this task are duplicates, skip the task: `gokyn task skip <taskId> --reason "All qualifying venues already have events"`
- **Only proceed to event creation if the search returns no matches for the chosen venue.**

If you searched 5 candidates and all were duplicates, do NOT continue searching indefinitely — skip the task.

### Step 6: Create the event

Look up the timezone from the State Timezone Reference table. Format open days as comma-separated numbers for `--recurrence-days`.

```bash
gokyn event create \
  --title "<venue name>" \
  --description "<2-3 sentence description per rules>" \
  --activity <activityId>:1 \
  --start-date-time "2027-01-01T09:00:00Z" \
  --end-date-time "2028-01-01T23:59:00Z" \
  --timezone "<timezone>" \
  --location-type physical \
  --location-place "<venue name>" \
  --location-address "<address>" \
  --location-lat <latitude> \
  --location-lng="<longitude>" \
  --recurring \
  --recurrence-frequency weekly \
  --recurrence-interval 1 \
  --recurrence-days "<open days>" \
  --is-public=false \
  --is-premium-only \
  --is-active=false \
  --price <price> \
  --price-currency USD \
  --booking-url "<venue website URL>" \
  --json
```

**CLI syntax notes:**
- Negative longitude MUST use `=` syntax: `--location-lng="-104.99"`
- Boolean false requires `=`: `--is-public=false`
- End date is always `2028-01-01T23:59:00Z` (one year window for recurring events)

Extract the `eventId` from the JSON response.

### Step 7: Generate and upload an event image (MANDATORY)

Every event must have an image. Use **one** of the following methods:

#### Option A: Use Kyndlo's built-in AI image generation (preferred)

```bash
gokyn image generate \
  --prompt "A welcoming <venue-type> with <atmosphere details>, inviting for casual social meetups. Inspired by <venue name> in <city>, <state>." \
  --event-id <eventId>
```

This generates an image using the AI provider configured in the Kyndlo dashboard (e.g. Gemini, OpenAI), optimizes it, uploads to R2, and attaches it to the event — all in one step.

#### Option B: Generate externally and upload

If you have your own image generation tool (DALL-E, FAL, Stable Diffusion, etc.), generate the image yourself, then upload:

```bash
gokyn image upload --file /tmp/venue-image.jpg --event-id <eventId>
# or from base64:
gokyn image upload --base64 "<base64-data>" --mime-type image/png --event-id <eventId>
```

#### Prompt guidelines (for either method)

- Describe the real venue type, atmosphere, and visual traits from your research
- Include the activity category (e.g. "arcade bar", "botanic garden", "comedy club")
- Mention key features: lighting, seating, mood, notable elements
- Keep it grounded in the real venue — don't invent unrelated scenes
- Example: "A lively retro arcade bar with neon lights, classic arcade cabinets, wood-fired pizza counter, and groups of friends playing games. Warm and inviting atmosphere in Orange Park, Florida."

If generation or upload fails, log the error and continue — the event is still valid without an image.

### Step 8: Complete the task

```bash
gokyn task complete <taskId> --event-id <eventId> --venue "<venue name>"
```

### Step 9: Track progress

Increment the batch counter. Log:

```
[Batch B, Task T/N] COMPLETED: <venue name> in <county> County (<cluster>/<category>) — Event ID: <eventId>
```

If the task was skipped:
```
[Batch B, Task T/N] SKIPPED: <county> County / <category> — Reason: <reason>
```

### Step 10: Check batch completion

If the batch counter has reached the batch size (**N**), go to **Batch Report**. Otherwise, loop back to Step 1.

---

## Batch Report

After completing each batch of **N** events, present a report to the user:

```
=== Batch <B> Report ===
Campaign:       <campaign-name>
City:           <current-city>
Batch size:     <N>
Created:        <count>
Skipped:        <count>
Failed:         <count>

Events Created:
  - <venue name> in <county> (<category>) — Event ID: <id>
  - ...

Skipped Tasks:
  - <county> / <category> — <reason>
  - ...

Cumulative Totals (all batches):
  Created: <total-created>  |  Skipped: <total-skipped>  |  Failed: <total-failed>
```

Then check remaining work:

```bash
gokyn task context --campaign <campaign> --city "<current-city>" --json
```

Report how many tasks remain in the current scope. Then ask:

> "Batch <B> complete. <X> tasks remaining in <city>. Continue with the next batch?"

**Wait for the user's response.**
- If **yes** — reset the batch counter, refresh rules, and resume the loop
- If **no** or **stop** — run Cleanup, then print the Final Summary
- If the user changes preferences (different city, county, batch size) — update the configuration and resume

---

## Error Recovery

| Error | Recovery |
|---|---|
| No tasks returned (count: 0) | If `diagnostic` field present, report it to the user — it may indicate stale in-progress tasks that need releasing. If city="any", rotate to next city. Otherwise stop the loop. |
| Diagnostic says tasks are "in_progress (possibly stale)" | Run `gokyn task release-stale --minutes 60` to release stuck tasks, then retry. |
| Duplicate event found | Skip venue, try next candidate. If all candidates are duplicates, skip the task with reason "All qualifying venues already have events". |
| No venues found | Try broader search terms. If still none, skip task. |
| No venues with determinable hours | Skip task with reason "No venues with published hours". |
| Activity ID not found | Try partial/shorter search terms. If still not found, skip task. |
| Event creation fails | Log the error. Release the task: `gokyn task release <taskId>`. Continue. |
| Photo download/upload fails | Continue without photo. Still complete the task. |
| gokyn task complete fails | Log the error. Release the task: `gokyn task release <taskId>`. Report the event ID. |
| Agent interrupted or unexpected error | Release all claimed-but-uncompleted tasks. See Cleanup. |

---

## Cleanup

Before exiting — whether normally or due to an error — release any task that was claimed but not completed or skipped.

```bash
gokyn task release <taskId>
```

If you have multiple uncompleted tasks, or if previous agents left stale tasks behind, use the bulk release command:

```bash
gokyn task release-stale --minutes 60
```

This releases all `in_progress` tasks that were assigned more than 60 minutes ago back to `pending`.

**Rule:** A task must NEVER be left in `in_progress` status when the agent exits. Every claimed task must end in one of three states:
- **completed** — event created successfully
- **skipped** — permanent failure (no venues, category not found)
- **released** (back to pending) — transient failure (API error, timeout)

Use `skip` for permanent failures. Use `release` for transient failures.

---

## Final Summary

After all batches are done (or the user stops), print a final session summary:

```
=== Event Creation Session Summary ===
Campaign:       <campaign-name>
State:          <state>
Cities worked:  <list of cities processed>
Total batches:  <B>
Total created:  <count>
Total skipped:  <count>
Total failed:   <count>

All Created Events:
  - <venue name> in <county> (<category>) — Event ID: <id>
  - ...

All Skipped Tasks:
  - <county> / <category> — <reason>
  - ...

All Failed Tasks:
  - <county> / <category> — <error>
  - ...
```

---

## Skipping a Task

```bash
gokyn task skip <taskId> --reason "No qualifying venue found in <county> County for <category>"
```

Always provide a specific reason.

## Releasing a Task

```bash
# Release a single task
gokyn task release <taskId>

# Release all stale tasks (assigned more than N minutes ago)
gokyn task release-stale --minutes 60
```

---

## Starting a New State

When a campaign needs to cover a new US state:

```bash
# 1. Register the state with its counties
gokyn task register-state --state "New York" \
  --counties "New York,Kings,Queens,Bronx,Richmond,Nassau,Suffolk"

# 2. Check city/metro areas
gokyn task cities --state "New York"

# 3. Seed the campaign
gokyn task seed --campaign "newyork-2027" --state "New York" \
  --counties "New York,Kings,Queens,Bronx,Richmond" \
  --clusters-json '{
    "intellectual": ["History Museums", "Bookstore Cafes"],
    "visionary": ["Escape Rooms", "Comedy Clubs"],
    "protector": ["Yoga Classes", "Botanic Gardens"],
    "creator": ["Art Museums", "Pottery Painting Studios"]
  }'

# 4. Verify
gokyn task campaigns
gokyn task context --campaign "newyork-2027"
```

---

## Event Validation Workflow

**CRITICAL: This is a MANDATORY step-by-step workflow for validating events. Follow each step in order.**

Validations are periodic re-checks of existing events to ensure venue data (hours, price, address, website, status) is still accurate. Events go stale over time — venues close, change hours, raise prices, or move. Your job is to verify each event against current real-world data and report issues.

### Validation Step 1: Check validation stats

```bash
gokyn validation summary
```

Report the summary to the user:
> "Validation queue: [total] total — [pending] pending, [valid] valid, [invalid] invalid, [needsUpdate] needs update, [overdue] overdue. Ready to start validating?"

**STOP and wait for the user's reply.**

### Validation Step 2: Ask preferences

**Say to the user:**
> "How many validations should I process before pausing to report? (e.g. 5, 10, 20). Would you like to filter by state or county?"

**STOP and wait for the user's reply.** Store batch size and optional filters.

### Validation Step 3: Claim next validation

```bash
gokyn validation next --assign --json
```

Add filters if specified: `--state <state>` and/or `--county <county>`.

If no validations returned, report to the user and stop.

Extract from the response:
- `_id` (validationId)
- `eventId`
- `eventTitle`
- `county`, `state`
- `status`, `priority`
- `lastValidatedAt` (when it was last checked)

### Validation Step 4: Fetch the event details

```bash
gokyn event get <eventId> --json
```

Extract the current event data:
- **title** — venue name
- **description**
- **location.address** — street address
- **location.place** — venue name at the location
- **location.coordinates** — lat/lng
- **price** — listed price
- **bookingUrl** — venue website
- **recurrence.daysOfWeek** — which days the event recurs
- **startDateTime** / **endDateTime**
- **activities** — linked activity categories

### Validation Step 5: Verify against real-world data

Use **goplaces** to look up the venue and compare:

```bash
goplaces search "<event title> in <county> County, <state>" --json --limit 3 --region US
```

Find the matching venue, then get full details:

```bash
goplaces details <place_id> --json
```

#### What to check:

| Field | How to verify | Issue field |
|-------|--------------|-------------|
| **Still open** | Check if the place is marked `permanently_closed` or not found | `other` |
| **Address** | Compare goplaces address with event `location.address` | `location.address` |
| **Hours** | Compare `regular_opening_hours.weekday_descriptions` with event `recurrence.daysOfWeek` | `recurrence.daysOfWeek` |
| **Price** | Check if entry fee has changed (from website if needed) | `price` |
| **Website** | Verify `bookingUrl` is still valid and points to the right venue | `bookingUrl` |
| **Name** | Check if the venue has been renamed | `other` |

#### Severity guidelines:

- **`error`** — Venue permanently closed, wrong address, completely wrong hours, broken/unrelated website
- **`warning`** — Minor hour changes (e.g. one day different), price changed slightly, website redirects but still works

### Validation Step 6: Submit the result

Based on your findings, submit one of three statuses:

#### If everything checks out:

```bash
gokyn validation submit <validationId> --status valid
```

#### If there are issues that make the event inaccurate:

```bash
gokyn validation submit <validationId> --status invalid \
  --issues-json '[{"field":"<field>","severity":"<error|warning>","description":"<what changed>","currentValue":"<value in our DB>","expectedValue":"<actual value>"}]'
```

Multiple issues can be reported in the array:

```bash
gokyn validation submit <validationId> --status invalid \
  --issues-json '[
    {"field":"recurrence.daysOfWeek","severity":"error","description":"Venue now closed on Mondays","currentValue":"0,1,2,3,4,5,6","expectedValue":"0,2,3,4,5,6"},
    {"field":"price","severity":"warning","description":"Entry fee increased","currentValue":"$0","expectedValue":"$10"}
  ]'
```

#### If minor updates are needed but the event is mostly correct:

```bash
gokyn validation submit <validationId> --status needs_update \
  --notes "Hours changed for summer season — now opens at 10am instead of 9am"
```

### Validation Step 7: Track progress

Log each result:

```
[Batch B, V/N] VALID: <event title> in <county> County — no issues
[Batch B, V/N] INVALID: <event title> in <county> County — <issue count> issues found
[Batch B, V/N] NEEDS_UPDATE: <event title> in <county> County — <notes summary>
```

If the venue was not found on goplaces at all:

```bash
gokyn validation submit <validationId> --status invalid \
  --issues-json '[{"field":"other","severity":"error","description":"Venue not found on Google Places — may be permanently closed"}]'
```

### Validation Step 8: Check batch completion

If the batch counter has reached the batch size, go to **Validation Batch Report**. Otherwise loop back to Validation Step 3.

---

### Validation Batch Report

After each batch, present:

```
=== Validation Batch <B> Report ===
Processed:      <count>
Valid:           <count>
Invalid:        <count>
Needs Update:   <count>

Results:
  - <event title> (<county>) — VALID
  - <event title> (<county>) — INVALID: <brief issue>
  - ...

Cumulative Totals (all batches):
  Valid: <total>  |  Invalid: <total>  |  Needs Update: <total>
```

Then check remaining:

```bash
gokyn validation summary
```

> "Batch <B> complete. <pending> validations remaining. Continue?"

**Wait for the user's response.**

---

## Browsing Activities and Events

```bash
gokyn activity list --search "yoga" --limit 10
gokyn activity list --category "wellness" --json
gokyn activity get <activityId>
gokyn activity categories

gokyn event list --limit 10
gokyn event list --search "garden" --is-active --json
gokyn event get <eventId>
```

## Updating and Deleting Events

```bash
gokyn event update <eventId> --title "New Title"
gokyn event update <eventId> --is-active=false
gokyn event update <eventId> --price 25 --price-currency USD
gokyn event update <eventId> --activity <id1>:1 --activity <id2>:2
gokyn event update <eventId> \
  --location-type physical \
  --location-place "New Venue" \
  --location-address "123 Main St" \
  --location-lat 40.7 \
  --location-lng="-74.0"
gokyn event delete <eventId>
```

---

## Geographic Queries

```bash
gokyn task states                      # List registered US states
gokyn task counties --state "Colorado" # List counties in a state
gokyn task cities --state "Colorado"   # List metro areas + rural breakdown
```

---

## Command Quick Reference

| Command | Purpose |
|---|---|
| `gokyn whoami` | Verify token and permissions |
| `gokyn task rules` | **Read event creation rules (MANDATORY before each batch)** |
| `gokyn task campaigns` | List campaigns with progress |
| `gokyn task context --campaign <id>` | Campaign progress, next county |
| `gokyn task summary --campaign <id>` | Detailed stats by city and county |
| `gokyn task cities --state <s>` | Metro areas and county mappings |
| `gokyn task next --campaign <id> --city <c> --assign --name <n>` | Claim next task |
| `gokyn task complete <id> --event-id <eid>` | Mark task done |
| `gokyn task skip <id> --reason <r>` | Skip impossible task |
| `gokyn task release <id>` | Unclaim a task |
| `gokyn task release-stale --minutes 60` | Release all stale in-progress tasks |
| `gokyn task seed --campaign <id> ...` | Seed tasks for counties |
| `gokyn activity list / get / categories` | Browse activities |
| `goplaces search "<query>" --json --limit 5 --region US` | **Search venues by category and location** |
| `goplaces details <place_id> --json` | **Get venue hours, address, coordinates** |
| `gokyn event list / get / create / update / delete` | Manage events |
| `gokyn image generate --prompt <p> --event-id <eid>` | **Generate AI image and attach to event** |
| `gokyn image upload --file <f> --event-id <eid>` | Upload venue photo from file |
| `gokyn validation next / submit / summary` | Event validation |

## Global Flags

| Flag | Env | Description |
|---|---|---|
| `--token <token>` | `KYNDLO_API_TOKEN` | API token (required) |
| `--base-url <url>` | `KYNDLO_API_URL` | API base URL (default: https://api.kyndlo.com) |
| `--json` | | Machine-readable JSON output |
| `--timeout <ms>` | | HTTP timeout in ms (default: 30000) |
| `--no-color` | `NO_COLOR` | Disable ANSI colors |

## Tips

- Always use `--json` when parsing output programmatically
- Always pass `--name` with `--assign` to track who claimed a task
- Use `--city` to focus on a metro area: `--city "Denver"` or `--city "Rural"`
- Negative numbers need `=` syntax: `--location-lng="-104.99"`
- Boolean flags: `--is-public` = true, `--is-public=false` = false
- IDs are 24-character hex strings (MongoDB ObjectId)
- Dates are ISO 8601: `2027-01-01T09:00:00Z`
