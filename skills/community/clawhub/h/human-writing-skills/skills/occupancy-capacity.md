# Occupancy and Capacity Skill

## Aim

Audit whether a physical support, slot, container, surface, or zone can plausibly hold the people or objects assigned to it.

This is a generic physical-world rule. Do not hardcode one vehicle layout, one chair type, or one seating convention. Infer capacity from the text, the ledger, and common affordances, then require an explicit transformation when capacity changes.

## Core Concept

Every occupied place is a physical resource.

Examples:

- vehicle seat, rear bench, folded seat, aisle, cargo area
- motorcycle saddle, sidecar, footrest
- airplane seat, aisle, galley, lavatory, overhead bin
- dining chair, booth bench, table edge, floor cushion
- stool, ladder, bed, sofa, floor, doorstep, lap

Each resource has:

| Field | Meaning |
| --- | --- |
| Resource name | The named place or support, such as rear-left zone, bench, stool, bed, aisle |
| Mode | seat, bed, bench, standing surface, storage, lap, folded, blocked, collapsed |
| Capacity rule | one adult, two children, shared bench, prone body, load-limited, unknown |
| Occupants/items | Who or what currently uses it |
| Posture | sitting, standing, lying, kneeling, leaning, crouching, straddling |
| Access path | how someone can enter, leave, or share it |
| Evidence | the text that established this state |

## Capacity Is Not Fixed

Do not assume every named place holds exactly one person.

Valid capacity changes include:

- two rear seats folded into a bed
- a bench that fits several people
- a child sitting on an adult's lap
- a person standing on a stool for a moment
- a narrow motorcycle saddle carrying driver and passenger
- passengers crowded in an aisle or on the floor
- objects moved away to free a surface

But each case needs textual evidence.

## Contradiction Gates

Flag a contradiction when:

1. Over-occupancy
   - A resource holds more people/items than its established mode permits.

2. Mode mismatch
   - A resource is used as a bed, standing platform, storage shelf, or shared bench without being established in that mode.

3. Missing transformation
   - Seats are folded, a table is cleared, a stool is climbed, a bed is made, or a motorcycle gains a passenger without an on-page transition.

4. Incompatible posture
   - A person is described as sitting, lying, standing, and blocked in ways the same resource cannot support at once.

5. Load or stability problem
   - A fragile chair, stool, branch, table, ladder, or narrow surface carries implausible load without acknowledgment.

6. Access-path conflict
   - A character reaches or enters an occupied/blocked resource without moving occupants, opening a path, climbing over, or changing posture.

7. Split-zone ambiguity
   - A broad label such as "rear-left", "corner", "by the table", or "on the bed" contains multiple occupants, but the text never clarifies whether it is a single slot, shared zone, layered posture, or transformed surface.

## Audit Questions

- What physical resource is being occupied?
- What mode is that resource currently in?
- What capacity did the text establish?
- Who or what is already there?
- Is the new occupant sharing, replacing, standing on, lying on, or passing through?
- Was a transformation or access path written?
- Could this be plausible if the description were clarified?

## Repair Options

- Clarify that the resource is a shared bench, bed, floor area, lap, aisle, or folded surface.
- Add a transformation beat: folded seats, moved bags, cleared table, stopped vehicle, opened aisle.
- Split a vague location into specific zones.
- Move a character to a plausible adjacent resource.
- Add pressure language if the over-occupancy is intentional: crowded, unstable, wedged, balancing, half-kneeling.

## Required Audit Output

```text
Occupancy/Capacity Review
| Resource | Mode | Capacity evidence | Current occupants/items | New claim | Pass/Fail | Reason |
```

## Principle

The standard is not "one seat, one person." The standard is: every physical resource must have a plausible current mode, capacity, occupancy, and access path.
