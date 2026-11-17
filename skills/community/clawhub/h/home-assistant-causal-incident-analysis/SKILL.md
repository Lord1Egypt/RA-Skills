---
name: "home-assistant-causal-incident-analysis"
description: "Trace Home Assistant incidents by correlating automations, logbook attribution, entity history, and device registry records."
---

# Home Assistant causal incident analysis

Use when a device changed state unexpectedly and Home Assistant may have acted directly or through an indirect control path.

## Procedure

1. Define the incident window and normalize all displayed timestamps to one timezone.
2. Inventory relevant entities from current states. Include the reported device, power/input/output telemetry, upstream sensors, switches, and automations.
3. Inspect automation and script definitions before querying long history. Search for each relevant entity, device name, and integration name. Record enabled state, trigger, conditions, target, delays, and mode.
4. Resolve ambiguous entity names through the entity and device registries. Map entity ID to platform, device ID, manufacturer, model, and user-visible name. Do not infer hardware identity from an alias alone.
5. Query history narrowly:
   - Start with one control entity and the incident window.
   - Add upstream trigger sensors and downstream telemetry only after finding a candidate path.
   - Request minimal responses without attributes when attributes are not needed.
   - Narrow the time window or split entities if output truncates.
6. Query the logbook for each state-changing control entity. Capture the context entity and context name; use them to attribute a transition to an automation when present.
7. Build a timestamped chain: upstream sensor change → automation decision → control switch transition → downstream device telemetry. Preserve gaps and polling delays instead of forcing exact simultaneity.
8. Separate evidence levels:
   - Direct: logbook attributes the transition to an automation.
   - Indirect: ordered state changes support a path through another switch or input.
   - Speculative: an internal reset, protection latch, relay, or hardware mechanism lacks direct telemetry.
9. Check measurement semantics before concluding. Distinguish voltage, power, enable-state, load, and availability sensors. Treat `unknown` or `unavailable` as missing evidence, not proof that hardware was off.
10. Check for common-cause events and alternate paths, including communication recovery, power cycling, other enabled automations, and physical wiring. Do not equate correlation with direct control.
11. Record recorder limits. If Home Assistant lacks the decisive measurement, name the required external observation rather than stretching a proxy sensor.

## Pitfalls

- Broad multi-day, multi-entity history dumps truncate and bury transitions.
- Friendly names can conceal that an entity controls a smart plug rather than the appliance feature under investigation.
- Integration recovery can restart an automation chain without directly controlling the reported device.
- Power telemetry cannot establish output voltage.
- A currently normal reading does not exclude an intermittent electrical fault.
- Never expose bearer tokens, registry identifiers, MAC addresses, or unrelated configuration values in the report.

## Verification

Before reporting a causal path, verify all three:

1. Static configuration proves the automation can target the identified control entity.
2. Logbook context attributes at least one relevant transition, or the report clearly labels attribution as unavailable.
3. Narrow history shows the claimed ordering inside the incident window.

Report the strongest supported conclusion, alternatives, missing decisive evidence, and the smallest safe measurement that would distinguish them.
