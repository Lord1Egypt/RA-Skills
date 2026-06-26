---
name: phone-charger-stash-map
displayName: "Phone Charger Stash Map"
version: "1.0.0"
description: "Create a room-by-room household phone charger stash map with cable type, outlet location, return spot, travel backup, and reset routine without device passwords, account information, tracking, or monitoring setup."
triggerKeywords:
  - phone charger stash map
  - charger location map
  - household cable checklist
  - phone charger organizer
  - where are the chargers
  - cable return spots
  - charging station map
  - family charger checklist
tags:
  - home
  - organization
  - chargers
  - household
  - checklist
license: "MIT-0"
language: "en"
hasExecutableCode: false
promptOnly: true
execution: "noExec"
---

# Phone Charger Stash Map

## Purpose

Use this prompt-only skill when a user wants a simple household map of where phone chargers, wall adapters, cables, power banks, and travel chargers live. The deliverable is a room-by-room stash map with cable type, assigned return spot, backup location, and a short reset routine.

This skill is for physical charger organization only. It does not request or record device passwords, account information, serial numbers, tracking settings, monitoring setup, device location sharing, or instructions to watch another person's device use.

## Safety Boundary

Do not ask for or include passcodes, device passwords, Apple ID, Google account details, phone numbers, private device identifiers, tracking permissions, location-sharing setup, monitoring apps, parental surveillance settings, or account recovery data.

Keep the output about physical charger inventory, labeling, room placement, cable compatibility, safe visibility, and return routines. For damaged chargers, keep advice basic and conservative: stop using visibly damaged, frayed, hot, sparking, or unreliable items and replace them with appropriate certified accessories.

## Core Principles

- Make chargers findable before leaving the house.
- Assign each cable a clear home base.
- Label by connector type, not by private device owner data.
- Keep travel and emergency backups separate from daily-use chargers.
- Reduce cable drift with a light weekly reset.
- Avoid tracking, monitoring, or account details entirely.

## Required Inputs

Ask only for organization details:

- Rooms or zones to include: kitchen, bedroom, entryway, office, car, backpack, guest room, living room, travel bag, or school bag.
- Connector types: USB-C, Lightning, Micro-USB, USB-A, MagSafe, wireless pad, power bank cable, or mixed.
- Charger types: wall plug, cable only, wireless pad, power bank, car charger, multi-port adapter, or travel cube.
- Current pain point: missing cables, wrong connector, slow charger, tangled drawer, no charger by the door, or travel charger disappearing.
- Number of daily-use charging spots desired.
- Backup spots needed: car, bag, desk, guest area, or emergency drawer.
- Labeling supplies available: tape, marker, cable tags, zip ties, drawer dividers, pouches, bins, or clips.
- Reset frequency: daily, weekly, after trips, before school week, or before work week.

If the user does not know connector names, describe them in plain language and leave a column for connector type to confirm.

## Workflow

1. **Inventory chargers.** Count wall plugs, cables, wireless pads, power banks, car chargers, and travel chargers.
2. **Identify cable types.** Label by connector type and charging role, not by private account or password information.
3. **Choose daily-use stations.** Assign chargers to practical spots such as bed, desk, kitchen counter, entry table, or sofa side table.
4. **Choose backup spots.** Set aside chargers for car, travel bag, backpack, office drawer, guest spot, or emergency drawer.
5. **Create return spots.** Give every charger a home base, pouch, clip, bin, drawer section, or hook.
6. **Flag damaged items.** Mark visibly damaged, frayed, overheating, sparking, or unreliable chargers as do-not-use and replace.
7. **Make the visible map.** Build a room-by-room list that can be posted near the entryway, drawer, or family command center.
8. **Add a reset routine.** Create a quick sweep for returning cables, checking travel backups, and replacing missing labels.
9. **Add a leaving-home check.** Include a short check for phone, charger, cable, and power bank if needed.

## Output Format

Return a phone charger stash map with these sections:

1. **Household Charging Goal**
   - Main annoyance to solve
   - Daily charging spots needed
   - Backup spots needed
   - Privacy note: no passwords, accounts, tracking, or monitoring
2. **Room-by-Room Charger Map**
   - Room or zone
   - Charger type
   - Connector type
   - Outlet or drawer location
   - Assigned return spot
   - Notes
3. **Daily-Use Stations**
   - Bedside
   - Desk
   - Kitchen or entry
   - Living room
   - Other user-provided zones
4. **Backup and Travel Stash**
   - Car charger
   - Travel pouch
   - Backpack or work bag
   - Guest charger
   - Emergency power bank
5. **Cable Type Key**
   - USB-C
   - Lightning
   - Micro-USB
   - Wireless pad
   - Other connector types provided by the user
6. **Label Plan**
   - Label wording
   - Tag or tape location
   - Color or symbol if useful
   - Return spot label
7. **Do-Not-Use Check**
   - Frayed cable
   - Bent connector
   - Hot or sparking plug
   - Unreliable charger
   - Replacement note
8. **Weekly Reset Routine**
   - Return chargers to home spots
   - Refill travel pouch
   - Untangle drawer
   - Check power bank charge
   - Replace missing labels
9. **Leaving-Home Mini Check**
   - Phone
   - Cable
   - Wall plug
   - Power bank if needed
   - Travel pouch returned after use

## Example Prompts

Copy any prompt below and paste it to your AI agent. Fill in your household details.

**Family charger map:**
> Our family of four is always hunting for phone chargers. We have USB-C and Lightning cables all over the house. Can you help me make a room-by-room charger stash map? I want to assign each cable a home spot: bedside, kitchen counter, living room, and entryway. Also need backup chargers for the car and travel bags.

**Declutter and reset:**
> Our charging drawer is a tangled mess of old cables. I want to inventory what we actually use, label each charger by connector type and return spot, and set up a simple weekly reset routine. I don't want any tracking, monitoring, or account stuff—just physical charger organization.

**Travel and backup plan:**
> I keep losing my travel charger between trips. Help me make a charger map that includes: daily charging stations at home, a dedicated travel pouch checklist, a car charger spot, and a leaving-home check so I don't forget my cable and power bank before work trips.

## Quality Bar

A strong result feels like a practical household map that ends charger hunting without creating surveillance, account, or password records. It should be easy to print, tape inside a cabinet, or place near the door, and it should make cable return habits visible.
