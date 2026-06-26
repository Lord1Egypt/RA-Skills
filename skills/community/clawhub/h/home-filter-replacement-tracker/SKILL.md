---
name: Home Filter Replacement Tracker
description: Build a household filter inventory with locations, sizes, replacement intervals, next due dates, shopping list, and reminders.
version: "1.0.0"
type: prompt-flow
tags:
  - home-maintenance
  - household-admin
  - filters
  - reminders
  - organization
author: OpenClaw Skill Library
---

# Home Filter Replacement Tracker

## Overview

Home Filter Replacement Tracker helps a household map every routine replaceable filter, record sizes and model details, set replacement intervals, calculate next due dates, and generate a shopping and reminder plan. It is designed for ordinary household organization, not risky repair work.

This skill does not override appliance manuals, landlord rules, lease requirements, building policies, or professional advice. It should not instruct the user to open sealed systems, bypass safety panels, or perform unsafe maintenance.

## When to Use

Use this skill when the user wants to:

- Track HVAC, furnace, air purifier, refrigerator, water, range hood, humidifier, vacuum, or similar household filters
- Build a replacement calendar
- Create a shopping list for filter sizes and models
- Remember when filters were last changed
- Standardize a household maintenance log
- Prepare questions for a landlord, property manager, technician, or manufacturer

**Trigger phrases:** "Track my home filters", "When should I replace filters?", "Make a filter replacement schedule", "Build a household filter list", "I need a filter shopping list"

## Required Inputs

Collect what the user already knows and mark unknowns clearly:

- Home systems or appliances with replaceable filters
- Filter location in the home
- Size, model number, brand, or compatible part number
- Purchase link or preferred store, if safely available
- Last replacement date or approximate date
- Manufacturer interval, if known
- Household factors that may shorten intervals, such as pets, smoke, dust, allergies, heavy cooking, or high usage
- Reminder preference, if relevant

Do not ask the user to take apart equipment or inspect unsafe areas.

## Workflow

### Step 1 - List Home Systems With Replaceable Filters

Create a broad inventory. Prompt the user to consider:

- HVAC return vents, furnace, central air, mini-split, or heat pump filters
- Air purifiers
- Refrigerator water and air filters
- Under-sink, countertop, whole-house, or pitcher water filters
- Range hood, microwave grease, or charcoal filters
- Humidifier or dehumidifier filters
- Vacuum filters
- Dryer lint screen and any replaceable dryer accessories
- Robot vacuum filters
- Bathroom fan or specialty ventilation filters, if applicable
- Any other appliance or system named by the user

Mark uncertain systems as "verify".

### Step 2 - Capture Location, Size, Model, Brand, and Purchase Source

For each filter, record:

- System or appliance
- Exact home location
- Filter size or part number
- Brand or compatible model
- Quantity needed
- Preferred purchase source or link
- Notes from the manual, label, landlord, or technician

If size or model is unknown, do not guess. Add a verification task such as "check label on existing filter" or "confirm in manual".

### Step 3 - Record Last Replacement Date

Ask for the last changed date. If unknown, use one of these labels:

- Exact date known
- Month known
- Season known
- Before move-in
- Unknown

For unknown or stale filters, recommend verification or replacement according to the manual and user circumstances, without presenting it as professional advice.

### Step 4 - Assign Replacement Intervals

Assign intervals using the best available source in this order:

1. Manufacturer manual or filter label
2. Landlord, property manager, technician, or building guidance
3. Household preference based on usage and conditions
4. Conservative placeholder interval marked for verification

Typical examples may be offered as placeholders only, such as monthly, every 2-3 months, every 6 months, or annually. Always flag placeholders that need confirmation.

### Step 5 - Build a 90-Day and 12-Month Calendar

Calculate next due dates from the last replacement date and interval. Produce:

- Filters due now
- Filters due in the next 30 days
- Filters due in the next 90 days
- 12-month replacement calendar
- Items with unknown dates requiring verification

If the current date is not known from context, ask for it or use the date supplied by the user.

### Step 6 - Generate a Shopping List

Create a consolidated shopping list:

- Filter name
- Size or model
- Quantity
- Preferred brand or compatible options
- Purchase source
- Needed by date
- Verification needed before buying

Group identical filters together to avoid duplicate purchases.

### Step 7 - Create a Replacement Log and Reminder Checklist

Provide a reusable log format with fields for:

- Date changed
- Filter replaced
- Location
- Size or model
- Quantity used
- Next due date
- Who changed it
- Notes, such as dust level, airflow issue, or manual reference

Add reminder checklist steps such as "confirm size before ordering", "buy spare", "replace", "record date", and "set next reminder".

### Step 8 - Flag Filters Needing Verification or Professional Help

List filters that need confirmation because:

- Size, part number, or location is unknown
- Access appears unsafe or restricted
- The system may be sealed, hardwired, high-voltage, high-pressure, or otherwise risky
- Landlord or building rules may apply
- Manual guidance conflicts with assumptions

Recommend checking the manual, asking the landlord, or contacting a qualified professional when appropriate.

## Deliverable Format

Return a household filter map in this structure:

```markdown
# Home Filter Replacement Tracker

## 1. Filter Inventory
| System | Location | Size/Model | Quantity | Last Changed | Interval | Next Due | Status |
|---|---|---:|---:|---|---|---|---|

## 2. Due Soon
- Due now:
- Next 30 days:
- Next 90 days:

## 3. 12-Month Calendar
- Month:
  - Filters due:

## 4. Shopping List
| Item | Size/Model | Quantity | Source | Needed By | Verify Before Buying |
|---|---|---:|---|---|---|

## 5. Replacement Log Template
| Date | Filter | Location | Size/Model | Next Due | Changed By | Notes |
|---|---|---|---|---|---|---|

## 6. Reminder Checklist
- Confirm model or size.
- Buy or stage replacement.
- Replace according to manual or allowed maintenance rules.
- Record date changed.
- Set next reminder.

## 7. Verification Flags
- Items needing manual, landlord, or professional confirmation:
```

If the user is on a platform where tables are awkward, use bullet lists instead.

## Safety Boundaries

- Do not override manuals, landlord instructions, lease terms, building rules, or professional advice.
- Do not instruct the user to open sealed systems, remove safety panels, access live electrical components, work around gas equipment, or perform risky maintenance.
- Do not claim that placeholder intervals are manufacturer-approved.
- Do not diagnose HVAC, water quality, appliance, mold, electrical, or air quality problems.
- If access is unsafe, restricted, unclear, or technically complex, recommend a qualified professional or responsible property contact.
- Do not collect unnecessary personal data, credentials, account access, or private home details beyond what is needed for the tracker.

## Acceptance Criteria

1. The deliverable includes locations, sizes or models, intervals, last-changed dates, next due dates, a shopping list, and reminders.
2. Unknown details are flagged instead of guessed.
3. The workflow includes a 90-day and 12-month view.
4. The result includes a reusable replacement log.
5. Safety boundaries prevent risky maintenance instructions.
6. Manual, landlord, and professional guidance take priority over generic intervals.
7. The skill remains prompt-only and requires no API, network access, credentials, or executable code.

## Example Prompts

1. **Full home inventory:** "We just moved into a house and I want to track every filter we need to replace. We have central HVAC, a fridge with water/ice, an air purifier in the bedroom, a range hood, and a vacuum. Help me build a replacement tracker."

2. **Shopping list for filter run:** "I'm heading to the hardware store this weekend and want a consolidated shopping list for all my home filters. I know my HVAC takes a 16x25x1, the fridge filter is a Whirlpool EveryDrop 1, and I think the air purifier needs a HEPA replacement but I'm not sure of the model."

3. **Calendar and reminders:** "I keep forgetting when I last changed the furnace filter. Can you help me set up a replacement calendar for all my household filters with next due dates and a simple reminder checklist?"

## Install-First Success Path

1. **Input:** User lists home systems or appliances with replaceable filters, provides known locations, sizes, model numbers, last replacement dates, and preferred intervals or reminder schedule.
2. **Steps:** Skill inventories all filter-equipped systems, captures location/size/model/brand for each, records last replacement dates (marking unknowns), assigns replacement intervals using manual/landlord/technician guidance as primary source, builds 90-day and 12-month calendars, generates a consolidated shopping list, creates a reusable replacement log format with reminder checklist, and flags filters needing verification or professional help.
3. **Output:** A Home Filter Replacement Tracker document with Filter Inventory table, Due Soon lists, 12-Month Calendar, Shopping List, Replacement Log Template, Reminder Checklist, and Verification Flags.
