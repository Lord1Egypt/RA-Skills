---
name: home-water-leak-first-hour-log
displayName: "Home Water Leak First Hour Log"
version: "1.0.0"
description: "Create a first-hour action log for home water leaks with shutoff checklist, photo checklist, damage notes, contacts, and cleanup timeline."
triggerKeywords:
  - water leak first hour
  - ceiling leak
  - pipe leak
  - appliance leak
  - fixture leak
  - water pooling
  - water dripping
  - emergency leak log
tags:
  - home-admin
  - urgent-home
  - water-leak
  - damage-documentation
  - incident-log
license: "MIT-0"
language: "en"
hasExecutableCode: false
promptOnly: true
execution: "noExec"
---

# Home Water Leak First Hour Log

## Purpose

Use this prompt-only skill when water is dripping, pooling, or spreading from a ceiling, pipe, appliance, fixture, wall, floor, or unknown source and the user needs a practical first-hour action log. The deliverable is a concise log with a shutoff checklist, photo checklist, damage notes, contact list, and cleanup timeline.

This skill helps the user document and organize immediate actions. It does not diagnose plumbing failures, give repair instructions, or replace emergency responders, a licensed plumber, electrician, landlord, building management, insurer, or restoration professional.

## Safety Boundary

Treat active flooding, sagging ceilings, structural danger, sewage, contaminated water, sparks, burning smell, shock risk, or water near outlets, breaker panels, appliances, cords, or standing electricity hazards as urgent. Tell the user to avoid standing water near electricity, leave unsafe areas, and call emergency help, building management, the utility, landlord, or qualified professionals as appropriate.

Do not instruct the user to open electrical panels, cut walls, work on live fixtures, disassemble appliances, climb into unsafe spaces, repair pipes, replace valves, use power tools near water, or perform restoration beyond basic safe containment and documentation. Do not promise insurance coverage or assign fault.

## When to Use

Use this skill when:

- Water is actively dripping, pooling, spreading, staining, or seeping inside a home.
- The user needs to remember what they did during the first hour.
- A landlord, building manager, plumber, insurer, restoration company, or neighbor may need a clear incident timeline.
- The user wants a printable or shareable checklist for photos, damage notes, contacts, and cleanup tracking.

Do not use it for non-urgent maintenance planning, plumbing repair instructions, mold remediation instructions, or insurance legal advice.

## Required Inputs

Ask only for details the user can provide safely:

- Current time, discovery time, and whether water is active, slowing, or stopped.
- Location of water and suspected source if known.
- Whether any electricity, ceiling sagging, contaminated water, or structural risk is present.
- Whether the main shutoff, fixture shutoff, appliance shutoff, or building contact is known.
- People, pets, valuables, furniture, electronics, documents, or rooms at risk.
- Photos already taken and visible damage.
- Contacts available: landlord, building manager, plumber, insurer, restoration company, neighbor, HOA, or emergency services.
- Cleanup actions already taken without adding repair instructions.

Mark unknowns clearly. If the situation is dangerous, prioritize safety instructions before asking for full details.

## Workflow

1. **Stabilize safety.** Identify electricity, structural, contaminated water, slip, or active flooding risks. Escalate urgent hazards before routine logging.
2. **Locate the apparent source.** Record where water is seen and what source is suspected, without diagnosing or giving repair steps.
3. **Shut off water if safe and known.** Create a checklist for main, fixture, appliance, or building shutoff status. If the user is unsure or access is unsafe, direct them to call the responsible contact or professional.
4. **Protect electricity and valuables.** Document whether the user avoided wet electrical areas, moved reachable valuables from dry ground only, and kept people and pets away from unsafe zones.
5. **Document photos.** Build a photo checklist covering source area, water path, affected rooms, damaged items, floors, ceilings, walls, labels, timestamps, and before or after cleanup shots.
6. **Record damage notes.** Capture room-by-room observations, materials affected, item list, odor, discoloration, ceiling or wall changes, and spreading pattern.
7. **Track contacts.** Log calls, messages, names, times, case numbers, instructions received, arrival windows, and next actions.
8. **Build cleanup timeline.** Record safe containment and cleanup actions, drying or fan placement if already done safely, removed wet items, professional cleanup plans, and follow-up checks.

## Output Format

Return a first-hour action log with these sections:

1. **Immediate Safety Check**
   - Active flooding status
   - Electricity or appliance risk
   - Ceiling, wall, floor, or structural concern
   - Contaminated or sewage water concern
   - People and pets clear of the area
   - Emergency, utility, landlord, building, or professional help needed
2. **Incident Snapshot**
   - Discovery time
   - Current time
   - Address or unit reference if the user wants to include it
   - Affected rooms or areas
   - Suspected source, marked as suspected if uncertain
   - Whether water is active, slowing, or stopped
3. **Water Shutoff Checklist**
   - Main shutoff location and status
   - Fixture shutoff status
   - Appliance supply shutoff status
   - Building or landlord shutoff contact
   - Who performed or confirmed shutoff
   - Time shutoff was attempted or completed
4. **Protective Actions Log**
   - Kept clear of standing water near electricity
   - Moved people, pets, and reachable valuables if safe
   - Contained water only where safe
   - Avoided unsafe repairs or electrical contact
   - Other immediate actions already taken
5. **Photo Checklist**
   - Wide shots of affected areas
   - Close shots of dripping, pooling, stains, damage, and water path
   - Source area if visible from a safe location
   - Damaged items and serial labels if relevant
   - Before, during, and after cleanup shots
   - Screenshots of messages, alerts, or case numbers
6. **Damage Notes**
   - Room-by-room damage table
   - Walls, ceilings, floors, cabinets, furniture, electronics, documents, clothing, and personal items
   - Odor, discoloration, swelling, sagging, or spreading pattern
   - Items moved, protected, discarded, or left in place
7. **Contact List and Call Log**
   - Emergency services, utility, landlord, building management, plumber, insurer, restoration company, neighbor, HOA, or other contacts
   - Time contacted
   - Person or department reached
   - Instructions received
   - Case, claim, work order, or ticket number
   - Follow-up owner and deadline
8. **Cleanup Timeline**
   - First 15 minutes
   - 15 to 30 minutes
   - 30 to 60 minutes
   - After first hour
   - Professional cleanup, inspection, or repair handoff notes
9. **Safety Note**
   - Avoid standing water near electricity. Call emergency help for active flooding, electrical hazards, structural danger, contaminated water, or any situation that feels unsafe. This log is for documentation, not repair instructions.

## Example Prompts

- "Water is dripping from the ceiling in my living room. Help me make a first-hour action log."
- "I just discovered a leak under the kitchen sink. Build a shutoff checklist and photo checklist."
- "There is water pooling around my washing machine. Create an emergency leak log with contacts and cleanup timeline."

## Quality Bar

A strong result helps the user act calmly, document what happened, and hand off the incident to the right people. It should be timestamped, easy to print, conservative on safety, and free of plumbing, electrical, or restoration repair instructions.
