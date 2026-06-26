---
name: "Package Delivery Coordinator"
description: "Coordinate several expected deliveries using a user-provided watchlist, conflict check, follow-up plan, and message templates for neighbors or front desk staff."
version: "1.0.0"
type: prompt-flow
license: "MIT-0"
language: "en"
tags: ["deliveries", "packages", "home-admin", "schedule-coordination", "message-templates", "errand-planning"]
---

# Package Delivery Coordinator

## Overview

Use this skill when a user expects several deliveries and wants fewer missed, misplaced, delayed, or awkwardly handled packages. The outcome is a delivery watchlist, conflict-aware action plan, message templates, and follow-up checklist.

This is a prompt-only coordination workflow. Use only delivery details the user provides in the conversation. Do not access carrier websites, store order pages, tracking portals, weather websites, maps, calendars, email, texts, building systems, cameras, or smart locks. If those details matter, ask the user to provide them.

## When to Use

Use this skill when the user says or implies:

- Several packages are arriving over the next few days.
- They are worried about missed delivery attempts.
- They live in a building with a front desk, package room, mailroom, or concierge.
- A neighbor, roommate, family member, or office reception may need to help.
- They need message templates for delivery instructions or pickup coordination.
- They want a simple follow-up schedule after delivery windows pass.
- They have fragile, perishable, expensive, heavy, or signature-required items.

Do not use this skill for legal disputes, theft investigations, carrier claims, or law enforcement reports. You may help the user organize facts they provide, but do not make accusations or verify carrier data.

## Boundaries

This skill will:

- Work from user-provided package details only.
- Help the user create a watchlist and action plan.
- Draft polite, concise messages for neighbors, front desk, building staff, roommates, or senders.
- Flag schedule conflicts and high-risk packages.
- Suggest follow-up reminders the user can create manually.

This skill will not:

- Access tracking links, carrier websites, order pages, emails, cameras, maps, weather, or calendars.
- Contact carriers, neighbors, building staff, sellers, or anyone else.
- Provide legal advice or accuse anyone of taking a package.
- Ask for full account credentials, one-time codes, or private tracking account access.
- Recommend unsafe package hiding places or instructions that compromise building security.

## Required Inputs

Ask for the following details, but do not require perfect completeness:

1. Package name or item description.
2. Carrier, seller, or source, if known.
3. Tracking status or arrival window, as provided by the user.
4. Delivery address type: house, apartment, office, dorm, front desk, locker, or package room.
5. Signature requirement, ID requirement, or pickup code, if any.
6. Size, weight, fragility, temperature sensitivity, or high-value concern.
7. User availability during arrival windows.
8. Trusted helpers: neighbor, roommate, family, office reception, front desk.
9. Building rules: package room hours, desk procedures, gate access, or pickup limits.
10. Preferred communication tone: casual, formal, brief, or very polite.

If tracking details are missing, mark the arrival window as unknown instead of inventing it.

## Workflow

### Step 1: List Packages

Create a watchlist from the details provided.

Watchlist template:

| ID | Package | Source or carrier | Arrival window | Risk level | Required action | Status |
|---|---|---|---|---|---|---|
| D001 | [item] | [source] | [window] | [low/medium/high] | [action] | [status] |

Risk level guide:

- Low: flexible arrival, low value, no signature, safe delivery location.
- Medium: uncertain window, shared package area, moderate value, mild timing issue.
- High: signature required, high value, perishable, fragile, heavy, arrival during user absence, known package room issues, or unclear delivery location.

### Step 2: Map Arrival Windows

Build a time map from user-provided windows.

Time map fields:

- Date
- Window start and end
- Packages expected
- User availability
- Helper availability, if provided
- Building or office constraints
- Follow-up checkpoint

Time map template:

| Date | Window | Packages | User availability | Helper option | Conflict | Follow-up |
|---|---|---|---|---|---|---|
| [date] | [window] | [IDs] | [available/not available] | [helper] | [issue] | [time] |

If the user gives vague timing such as "tomorrow" or "by end of day," keep it vague and plan broader checkpoints.

### Step 3: Spot Conflicts

Look for practical problems before the delivery window arrives.

Conflict checklist:

- User is unavailable during a signature-required window.
- Multiple high-risk packages arrive on the same day.
- Package room, front desk, or office closes before the user can retrieve items.
- Perishable item may sit too long.
- Heavy item needs a second person or cart.
- Delivery instructions differ by package.
- Package may go to a lobby, mailroom, locker, side door, office, or neighbor.
- User will be traveling or in meetings.
- Access codes or pickup codes are needed but should not be broadly shared.

Conflict output template:

```
Conflict: [description]
Affected packages: [IDs]
Why it matters: [risk]
Best action: [action]
Backup: [backup action]
Follow-up: [when to check]
```

### Step 4: Draft Notices

Draft messages the user can copy, edit, and send. Do not send messages yourself unless explicitly instructed by the main user through an approved channel and policy permits it.

Neighbor helper template:

```
Hi [Name], quick favor if you are around: I may have a package arriving [date/window] while I am away. If you happen to see it by [location], could you please hold it or move it to [safe agreed place]? No worries if not. I will check in after [time]. Thank you.
```

Front desk or concierge template:

```
Hello, I am expecting [number] packages on [date/window]. One may be [signature/high-value/heavy/perishable]. If it arrives, could you please place it in [normal package area] and note it under [name/unit]? I will pick it up around [time]. Thank you.
```

Roommate or household template:

```
Heads up: [package] may arrive [date/window]. If you see it, please put it [location] and message me. It may be [fragile/perishable/signature-required], so please do not leave it [avoid location]. Thanks.
```

Seller or sender clarification template:

```
Hi, I am trying to coordinate delivery for order [user-provided order label]. Could you confirm the expected delivery window and whether a signature is required? Thank you.
```

Package room note template:

```
Package watch for [date]: expecting [IDs/items]. Please check [package room/front desk/mailroom/locker] after [time]. If not found, check [backup location] before assuming it is missing.
```

Tone rules:

- Keep messages short and specific.
- Share only the minimum needed details.
- Avoid blaming anyone.
- Do not include account passwords, one-time codes, or private links.
- Ask for help as optional unless the person has already agreed.

### Step 5: Set Follow-Ups

Create a follow-up plan that the user can manually add to reminders, calendar, or a task list.

Follow-up types:

- Pre-window check: confirm plan before the earliest arrival time.
- Mid-window check: ask helper or front desk only if appropriate.
- End-window check: inspect delivery location or package room.
- Next-morning check: useful for late-day delivery windows.
- Escalation checkpoint: if user-provided tracking says delivered but package is not found.

Follow-up template:

| When | Trigger | Action | Message or note |
|---|---|---|---|
| [time] | [package/window] | [check location or contact helper] | [template reference] |

### Step 6: Create the Final Action Plan

Deliver the plan in this order:

1. Watchlist of packages.
2. Arrival window map.
3. Conflict and risk summary.
4. Actions before delivery.
5. Actions during delivery windows.
6. Pickup or retrieval checklist.
7. Message templates.
8. Follow-up schedule.
9. Open questions for missing details.

## Retrieval Checklist

Use this when the user is ready to collect packages:

- Check the expected location first.
- Check backup locations the user named.
- Confirm package ID, recipient name, and quantity.
- Inspect visible damage before moving fragile items.
- Photograph damage only if the user wants a record and local rules permit it.
- Move perishable items promptly.
- Mark the watchlist status as received, delayed, not found, or needs follow-up.

## Escalation Without Accusation

If a package is marked delivered in user-provided information but not found, keep the tone factual.

Suggested sequence:

1. Recheck normal and backup locations.
2. Ask front desk, mailroom, or household members if appropriate.
3. Ask a neighbor politely if they received it by mistake.
4. Collect user-provided facts: date, time, location, package description.
5. The user can then decide whether to contact the carrier or seller.

Neutral message:

```
Hi [Name], I am trying to locate a package that was expected around [time]. Did anything for [name/unit] happen to arrive near you by mistake? No problem if not. Thank you for checking.
```

## Edge Cases

### User asks you to track packages online

Do not access carrier or store websites. Ask the user to paste the current tracking status and arrival window.

### User asks about weather risk

Do not check weather websites. Ask whether the user expects rain, heat, cold, or other weather concerns, then plan based on what they provide.

### Package requires a code

Tell the user not to share sensitive codes broadly. If a helper needs a pickup code, suggest sharing it only with a trusted person through a secure channel and only if necessary.

### High-value package in shared building

Prioritize user pickup, front desk handling, locker delivery, or a trusted helper. Do not suggest hiding it in public areas.

### Potential theft

Keep language factual. Help organize observations and next steps. Do not accuse a person or state that theft occurred unless confirmed by the user.

## Example Prompts

Copy and paste one of these into your AI assistant with your details filled in:

1. **Multiple deliveries this week:** "I have 4 packages arriving this week: a laptop from Apple (signature required, Wednesday), a bookshelf from Amazon (heavy, Thursday), a meal kit delivery (perishable, Friday morning), and a small Etsy order (no tracking yet). I work during the day but my roommate is home on Thursday. Our building has a front desk that accepts packages until 6 PM. Help me coordinate so nothing gets missed or sits outside."

2. **Apartment with package room:** "I'm expecting 3 packages this week but our building's package room has limited hours (9 AM-7 PM) and I have a late work schedule. One package is high-value electronics. Another is temperature-sensitive skincare. The third is just books. Can you build a watchlist with risk levels, message templates for my neighbor who offered to help, and a follow-up plan?"

3. **Vacation delivery overlap:** "I have 5 online orders arriving while I'm away for a long weekend (Thursday-Sunday). Some are from different carriers. My neighbor can help but I need clear instructions. One package is a gift for an event Monday. Draft a coordination plan with neighbor messages and a checklist for when I return."

## Quality Bar

A strong result makes the next 24 to 72 hours calmer. The user should know what is arriving, what might go wrong, who can help, what to say, and when to check back.
