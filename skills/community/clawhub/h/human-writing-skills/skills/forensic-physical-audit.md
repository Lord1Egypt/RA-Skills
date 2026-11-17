# Forensic Physical Audit Skill

## Aim

Catch physical continuity errors in an existing draft by extracting evidence before judging. This skill is stricter than a generation guard: it treats the passage as a scene file to be audited.

## Core Rule

Do not say "pass" until every relevant physical claim has been extracted into tables.

## Evidence Extraction

Read the draft once only to collect evidence. Do not repair yet.

Extract these claims in chronological order:

| Beat | Text evidence | Character/object | Claim type | State |
| --- | --- | --- | --- | --- |
|  |  |  | position / facing / barrier / reach / contact / clothing / shoes / prop / injury |  |

Claim types:

- position: front seat, rear seat, driver side, outside car, doorway, bed, table, etc.
- relative position: in front of, behind, beside, between, across from
- barrier: soundproof glass, partition, locked door, seat back, table, seat belt
- reach/contact: touches, grabs, hands over, leans against, whispers directly, kisses, intimate contact
- sightline: sees directly, sees in mirror, looks back, cannot see
- clothing/shoes: short skirt, long skirt, flats, heels, coat on/off
- prop: phone, bag, envelope, keys, weapon, cup, cigarette
- body state: injury, restraint, wet/dry, makeup, blood, fatigue
- occupancy/capacity: who or what is on/in the same resource, how many, in what mode

## Contradiction Gates

Flag a contradiction when any of these appear:

0. Occupancy/capacity conflict
   - A physical resource holds more occupants/items than its established mode permits, or a broad zone receives multiple occupants without clarifying whether it is a shared surface, separate sub-slots, lap, bed, floor, aisle, or transformed resource.

1. Position drift
   - A character moves from front to rear, rear to front, outside to inside, or one side to another without an on-page movement beat.

2. Barrier violation
   - A character reaches, touches, whispers directly, or performs close contact across a partition, soundproof glass, locked door, seat back, or other barrier without a described workaround.

3. Reach impossibility
   - A character touches or manipulates something outside their plausible reach from the established seat, posture, or room position.

4. Sightline impossibility
   - A character sees something that their position, facing, barrier, darkness, or mirror angle would not allow.

5. Clothing/shoe drift
   - Shoes, skirt length, coat, hair, makeup, or accessories change without a change beat or time skip.

6. Prop drift
   - A prop appears, disappears, changes owner, or changes location without being moved on-page.

7. Body-state reset
   - Injury, fatigue, restraint, wetness, dirt, makeup, or physical limitation vanishes without a recovery/change beat.

8. Unsupported transformation
   - A seat, table, stool, bed, aisle, or surface changes function without an on-page transformation beat.

## Severity

- Critical: impossible action changes the scene outcome.
- Major: reader can notice the contradiction and lose spatial trust.
- Minor: detail drift that should be corrected but does not alter action.

## Required Output

```text
Physical Continuity Forensic Audit

1. Evidence Table
| Beat | Evidence | Claim | State |

2. Contradictions
| Severity | Type | Earlier state | Later conflict | Why impossible | Minimal fix |

3. State Ledger After Audit
- Occupancy/capacity:
- Character positions:
- Clothing/shoes:
- Props:
- Barriers:

4. Repair Plan
- Keep:
- Change:
- Add transition beat:
```

## No-Excuse Checks

In vehicle scenes, explicitly check:

- Who is in the driver seat?
- Who is in the front passenger seat?
- Who is rear-left, rear-center, rear-right?
- Are rear-left/rear-right separate one-person slots, a bench, a bed, a folded surface, or an unclear zone?
- Is there a partition or soundproof glass?
- Can the touching/contact action happen from those positions?
- Did anyone unbuckle, stop the car, climb over, exit, or re-enter?
- Did clothing and shoes stay the same?

In non-vehicle scenes, explicitly check the equivalent resources:

- What is the support or container: chair, stool, bench, bed, table, floor, aisle, motorcycle saddle, airplane seat?
- What mode is it in: sitting, standing, lying, storage, folded, collapsed, shared, blocked?
- How many occupants/items can that mode plausibly hold?
- Was sharing or transformation established?

## Avoid

- vague notes like "space is a little unclear"
- trusting the latest paragraph over earlier evidence
- repairing by silently moving characters
- treating erotic, violent, or high-emotion action as exempt from physical constraints
