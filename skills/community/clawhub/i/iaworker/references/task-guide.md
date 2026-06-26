# iaworker References

Additional context, templates, and domain knowledge for iaworker.

## Task Analysis Templates

### Repair Task Template

When analyzing a repair task, the step engine produces steps structured as:

```
[PREREQUISITES] → [ASSESSMENT] → [FIX] → [VERIFICATION] → [CLEANUP]
```

Each repair step should specify:
- **Tools** — what is physically needed
- **Time estimate** — realistic duration
- **Difficulty** — easy / medium / hard / expert
- **Safety warning** — any hazards
- **Common mistakes** — what to avoid

### Debug Task Template

Debug flows prioritize systematic narrowing:

```
[SECURE] → [REPRODUCE FAULT] → [ISOLATE SUBSYSTEM] → [IDENTIFY ROOT CAUSE] → [FIX] → [TEST]
```

Key debug principle: always reproduce the fault before attempting to fix it.

### Assembly Task Template

Assembly flows use a build-up pattern:

```
[SORT HARDWARE] → [PRE-ASSEMBLE SUB-GROUPS] → [JOIN] → [ALIGN + TORQUE] → [FINAL CHECK]
```

Key assembly principle: hand-tight first, fully torque last. Never fully tighten until alignment is confirmed.

---

## Domain Quick References

### Bike — Common Failure Map

| Symptom | Likely Cause | Tools |
|---------|-------------|-------|
| Chain skips | Chain stretched, cog worn | chain tool |
| Brake squeal | Pad contamination, glazing | sandpaper |
| Gear won't shift | Derailleur misalignment | hex keys |
| Wobble | Loose axle, warped rim | hex keys |
| Creak | Bottom bracket loose | crank puller |
| Flat tire | Puncture, valve worn | tire levers |

### Car — Common Failure Map

| Symptom | Likely Cause | Tools |
|---------|-------------|-------|
| No start | Battery, fuel, immobilizer | multimeter, OBD2 |
| Engine miss | Spark plugs, coils | spark plug socket |
| Brake squeal | Worn pads | jack, socket set |
| Overheating | Coolant, thermostat, pump | coolant, basic tools |
| Oil leak | Valve cover, oil pan | socket set, sealant |

---

## Prompt Engineering for Analysis

When iaworker needs to analyze an image frame, the analysis prompt should:

1. **Name the object** — what is the main subject?
2. **Note the condition** — is it new, used, damaged?
3. **Identify anomalies** — what's wrong or unusual?
4. **Estimate task type** — repair / debug / assembly / inspection?
5. **List tools likely needed** — based on the domain

Example frame analysis output:
```
Object: mountain bike, rear wheel
Condition: moderate use, some scratches on frame
Anomalies: chain appears loose (sagged), rear brake pad near end-of-life
Task: repair (chain tension + brake pad replacement)
Tools: hex keys (5mm), chain tool, replacement brake pads
```

---

## Safety Checklists

### Pre-Work Safety (Universal)

- [ ] Object is powered off / isolated
- [ ] Battery disconnected (for vehicles/electronics)
- [ ] Secured against tipping or rolling
- [ ] Adequate lighting in place
- [ ] Safety equipment nearby (gloves, glasses)

### Electrical Safety (Cars/Electronics)

- [ ] Negative battery terminal disconnected first
- [ ] Wait 5 min after disconnect before working (capacitor discharge)
- [ ] Never work on wet surfaces with power on
- [ ] Use insulated tools for high-voltage

### Mechanical Safety

- [ ] Bike: flipped or on repair stand
- [ ] Car: parking brake set, wheels chocked
- [ ] Never rely on a single jack point — use jack stands
- [ ] Keep fingers clear of pinch points

---

## Difficulty Rating Guidelines

| Rating | Criteria |
|--------|----------|
| **easy** | No special tools, minimal disassembly, low injury risk |
| **medium** | Basic hand tools, some disassembly, moderate care needed |
| **hard** | Specialty tools, significant disassembly, components under tension/spring |
| **expert** | Professional-grade tools, structural disassembly, safety-critical systems |

Time estimates should reflect a competent DIYer, not a beginner.
