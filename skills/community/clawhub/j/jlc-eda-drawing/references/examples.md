# Examples

Use this to map user requests to the right references.

## Request: "Deploy Run API Gateway"

Load:

- `bridge-api.md`

Expected behavior:

- Download or locate the official API package.
- Install Node dependencies if needed.
- Start the bridge server in the background.
- Verify `/health`.
- Confirm an EasyEDA window is connected.

## Request: "Draw a simple circuit"

Load:

- `design-standards.md`
- `parts-strategy.md`
- `eda-code-patterns.md`

Expected behavior:

- Prefer real parts such as resistor, LED, switch, connector.
- Create a named page if needed.
- Place parts, read pins, connect nets, label power and ground.
- Verify components and recent wire net names.

## Request: "Draw an ESP32 development board"

Load:

- `design-standards.md`
- `parts-strategy.md`
- `circuit-blocks.md`
- `eda-code-patterns.md`

Expected behavior:

- Include ESP32 module, USB-C or USB input, USB-UART, 3.3 V regulator, EN/BOOT, decoupling, power LED, and headers unless the user specifies a smaller scope.
- Use real LCSC/JLC parts.
- Expose UART and useful GPIOs.

## Request: "Make this PCB-ready"

Load:

- `design-standards.md`
- `parts-strategy.md`
- `pcb-workflow.md`

Expected behavior:

- Ensure each meaningful component has footprint metadata.
- Confirm connector polarity and pin labels.
- Prepare nets and blocks so PCB transfer/layout is clean.

## Request: "Route or check the PCB"

Load:

- `bridge-api.md`
- `pcb-workflow.md`
- `eda-code-patterns.md`

Expected behavior:

- Confirm PCB document context.
- Use PCB units.
- Place/reroute with mechanical intent.
- Run DRC when available.
