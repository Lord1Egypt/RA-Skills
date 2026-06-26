---
name: Last-Minute Travel Doc Pack
description: Organize urgent travel papers into a destination-ready packet and print/download checklist without storing private ID numbers.
version: "1.0.0"
type: prompt-flow
tags:
  - travel-documents
  - last-minute-travel
  - admin-logistics
  - packing-checklist
  - document-organization
author: OpenClaw Skill Builder
---

# Last-Minute Travel Doc Pack

## Overview

Last-Minute Travel Doc Pack helps a user who is leaving soon gather, sort, print, and download the papers they may need for a trip. It produces a destination-ready packet list and checklist organized by traveler, destination, and order of use.

This skill does not store passport numbers, national ID numbers, visa numbers, ticket numbers, or other private identifiers. It helps the user identify document types and missing items, not record sensitive values.

## When to Use

Use this skill when the user is close to departure and needs travel papers organized quickly, such as:

- International trip tomorrow or this week
- Family or group travel documents are scattered
- Need to know what to print versus save offline
- Need to sort documents by traveler
- Need a final airport or border packet order

**Trigger phrases:** "I leave tomorrow and need my travel documents", "help me organize travel papers", "last-minute passport and visa checklist", "what should I print for my trip", "make a travel doc packet".

## Deliverable

Produce a **Destination-Ready Travel Document Pack** with:

1. Trip snapshot
2. Traveler-by-traveler document list
3. Destination and transit requirements to verify
4. Print checklist
5. Offline download checklist
6. Missing item tracker
7. Packet order for airport, border, lodging, and return
8. Final departure check

## Workflow

### Step 1 - Identify the Trip

Ask only the minimum needed to build the pack:

- Departure date and time
- Departure country or region
- Destination country or region
- Transit countries or airports, if any
- Travelers and age categories, such as adult, child, infant, or pet
- Travel mode, such as flight, train, cruise, or car
- Trip purpose if relevant, such as tourism, work, study, family visit, or medical travel

Do not ask for passport numbers, national ID numbers, visa numbers, ticket numbers, payment card numbers, or full birth dates.

### Step 2 - List Required Papers

Build a checklist by document type. Include items that commonly apply, while reminding the user to verify official requirements for the destination and carrier:

- Passport or accepted ID
- Visa, electronic travel authorization, residency permit, or entry approval
- Flight, train, cruise, or transport booking
- Hotel or host address confirmation
- Travel insurance certificate
- Health, vaccine, prescription, or medical clearance documents if applicable
- Minor travel consent letter if a child travels without both legal guardians
- Pet documents if traveling with an animal
- Driver license and international driving permit if driving
- Event, school, work, invitation, or conference letters if relevant
- Return or onward travel proof if required
- Emergency contact sheet

### Step 3 - Sort by Traveler

Create one section per traveler. For each person, list:

- Must-have identity and entry documents
- Transport documents
- Lodging and itinerary documents
- Health or prescription documents, if applicable
- Special documents, such as child consent, accessibility support, or work letter
- Missing or uncertain items

Use document labels, not private numbers. Example: "Passport, valid for required period" instead of recording the passport number.

### Step 4 - Mark Missing Items

Create a missing item tracker with urgency levels:

- **Critical before departure:** likely blocks travel, boarding, or entry
- **Important:** may cause delays, fees, or extra screening
- **Helpful:** improves convenience or backup readiness

For each missing item, include the next action, owner, and deadline.

### Step 5 - Create Print and Download Checklists

Separate items into:

- **Print:** documents that may be required on paper or are useful when phones fail
- **Download offline:** documents needed when airport, hotel, or roaming internet is unreliable
- **Carry original:** identity, legal, or official documents that cannot be replaced by a copy
- **Backup copy:** photocopy or digital copy stored safely, without exposing sensitive numbers in chat

Recommend keeping sensitive originals secure and separate from backup copies where practical.

### Step 6 - Create Pack Order

Arrange the packet in the order the user may need it:

1. Departure airport or station
2. Security and boarding
3. Transit border or connection
4. Destination immigration or entry
5. Customs or health checks
6. Ground transport
7. Lodging check-in
8. Activities, work, school, or events
9. Return trip
10. Emergency backups

Add a compact "grab first" section for the documents most likely needed in the first two hours of travel.

## Output Template

```markdown
# Destination-Ready Travel Document Pack

## Trip Snapshot
- Departing:
- Destination:
- Transit:
- Travelers:
- Travel mode:
- Time until departure:

## Verify Official Requirements
- Destination entry rules:
- Transit rules:
- Carrier rules:
- Passport or ID validity period:
- Health, customs, or special requirements:

## Traveler Document Lists
### Traveler 1: [Name or label]
- Carry original:
- Print:
- Download offline:
- Backup copy:
- Missing or uncertain:

### Traveler 2: [Name or label]
- Carry original:
- Print:
- Download offline:
- Backup copy:
- Missing or uncertain:

## Missing Item Tracker
| Item | Traveler | Urgency | Next action | Owner | Deadline |
|---|---|---|---|---|---|
| [Item] | [Traveler] | Critical / Important / Helpful | [Action] | [Owner] | [Time] |

## Packet Order
1. Grab first:
2. Departure airport or station:
3. Transit:
4. Destination entry:
5. Lodging and ground transport:
6. Return trip:
7. Emergency backups:

## Final Departure Check
- Originals are packed in a secure place
- Printed copies are sorted by traveler and packet order
- Offline copies are available without internet
- Missing critical items are resolved or explicitly acknowledged
- Private ID numbers were not stored in this chat or document
```

## Safety Boundaries

- Do not store passport numbers, national ID numbers, visa numbers, ticket numbers, payment card details, or full birth dates.
- Do not claim to verify current entry rules unless reliable official sources have actually been checked in the current session.
- Do not guarantee boarding, visa approval, entry, or customs clearance.
- For official requirements, instruct the user to verify with the destination government, transit authority, airline, cruise line, rail operator, embassy, or consulate as appropriate.
- Do not advise falsifying documents, bypassing border rules, hiding restricted items, or misrepresenting identity or purpose of travel.
- For urgent missing documents that may block travel, clearly label the risk and suggest contacting the carrier or official authority.

## Acceptance Criteria

1. Identifies trip timing, destination, transit, travelers, and travel mode.
2. Produces a document checklist relevant to destination, transit, carrier, traveler type, and trip purpose.
3. Sorts documents by traveler without storing private identifier numbers.
4. Marks missing items with urgency, next action, owner, and deadline.
5. Separates carry-original, print, download-offline, and backup-copy items.
6. Creates a packet order for airport, border, lodging, return, and emergency use.
7. Includes official-requirement verification reminders and no guarantees of entry.
8. Produces English-only prompt-flow content with no executable code.

## Example

**User says:** "We fly tomorrow from Canada to Italy through Germany with two adults and one child. Our papers are scattered. Help."

**Skill response:** Build a Destination-Ready Travel Document Pack. Capture departure time, travelers, transit, and travel mode. List passports, entry authorization or visa status to verify, flight booking, lodging address, travel insurance, child consent if relevant, health or prescription documents, offline copies, printed copies, and a missing item tracker. Sort by traveler and create a packet order for departure, transit, destination entry, lodging, return, and emergency backups.

## Example Prompts

Copy and paste one of these prompts to get started:

**Prompt 1 — Family international trip:**
> We fly tomorrow from Canada to Italy through Germany with two adults and one child. Our papers are scattered across emails, apps, and a folder. Help me build a travel document pack sorted by traveler.

**Prompt 2 — Solo business travel:**
> I'm leaving tonight for a work trip to Singapore with a layover in Hong Kong. I need my passport, visa, work invitation letter, hotel confirmation, travel insurance, and return flight proof organized. Create a grab-and-go document checklist.

**Prompt 3 — Multi-destination with pet:**
> We're driving from the US to Canada with our dog for a week-long trip. I need to know what documents to carry for each traveler including the pet, what to print, and what to download offline.
