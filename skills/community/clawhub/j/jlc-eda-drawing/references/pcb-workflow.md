# PCB Workflow

Use this when the user asks for PCB layout, routing, DRC, or board-ready work.

## Context

- Confirm a PCB document is active or open/create one.
- Use PCB APIs only in PCB context.
- PCB units: `1 unit = 1 mil`.
- Schematic units: `1 unit = 0.01 inch`.

## Placement Heuristics

- Put connectors at board edges with the mating direction clear.
- Keep USB connectors accessible and align with enclosure intent if known.
- Place decoupling close to IC power pins.
- Keep crystals close to MCU oscillator pins.
- Keep antenna keepout clear for RF modules.
- Keep regulators and high-current paths short and thermally sane.
- Place programming/debug headers where probes can reach them.

## Routing Heuristics

- Route power and ground strategy before fine signals on simple boards.
- Keep USB D+/D- paired and short.
- Keep switching regulator hot loops compact.
- Avoid routing under RF antenna regions.
- Use pours for ground when appropriate.

## API Examples

```javascript
await eda.pcb_PrimitiveLine.create("GND", 1, 0, 0, 1000, 0, 10, false);
return await eda.pcb_Drc.check(true, true, false);
```

## Validation

- Run DRC if available.
- Check board outline, mounting holes, connector access, and polarity markings.
- Confirm critical nets reached intended pads.
