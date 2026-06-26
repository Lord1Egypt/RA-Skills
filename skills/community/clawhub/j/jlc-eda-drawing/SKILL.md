---
name: jlc-eda-drawing
description: Advanced JLC EDA / EasyEDA circuit design agent for schematic and PCB-ready work. Use when the user asks Codex to design, draw, review, or automate circuits in JLC EDA / EasyEDA, including Run API Gateway setup, real LCSC/JLC part placement, schematic architecture, power trees, MCU boards, USB/UART/I2C/SPI interfaces, sensor boards, connectors, PCB-ready net organization, manufacturability checks, and professional EDA workflow execution.
---

# JLC EDA Drawing

Act as a circuit-design copilot, not just an API caller. Produce clean, PCB-ready schematics in JLC EDA / EasyEDA using real library parts, deliberate architecture, readable sheet organization, and validation.

## Core Model

Use three layers:

1. **Bridge layer**: connect Codex to the running EasyEDA client.
2. **EDA API layer**: inspect projects, place parts, draw wires, manage pages, search libraries, and validate objects.
3. **Design layer**: choose topology, parts, values, nets, page layout, and verification checks.

Prefer MCP tools when available. Use the official API bridge package only as fallback or for reference.

## Design Intake

Move decisively when the request is clear. Ask one concise question only when a decision changes the circuit materially:

- Input/output voltage or current is unknown for power designs.
- MCU/module variant is ambiguous and affects pins or footprint.
- Connector, package, or mounting style matters mechanically.
- Safety, mains voltage, battery charging, RF, high current, or precision analog is involved.

Otherwise choose conservative defaults and state assumptions at the end.

## Reference Files

Load only what the task needs:

- `references/bridge-api.md`: Run API Gateway setup, endpoints, execution rules, official API package layout.
- `references/design-standards.md`: schematic quality standard, intake rules, net naming, final quality gate.
- `references/parts-strategy.md`: part search patterns and selection rules.
- `references/circuit-blocks.md`: reusable USB-C, regulator, MCU, UART, I2C, SPI, LED block rules.
- `references/eda-code-patterns.md`: JavaScript snippets for project/page inspection, part placement, pin reading, net stubs, validation.
- `references/pcb-workflow.md`: PCB context, units, placement/routing heuristics, DRC workflow.
- `references/examples.md`: concrete user requests and which reference files to load.
- `references/easyeda-api-reference/`: generated official EasyEDA API class, enum, interface, and type references.
- `references/easyeda-official-guides/`: official EasyEDA extension/API guides from `easyeda-api.zip`.
- `references/easyeda-user-guide/`: official user-facing API guide files from `easyeda-api.zip`.
- `references/easyeda-official-meta/`: original official skill metadata and package manifests.
- `scripts/bridge-server.mjs`: bundled official Run API Gateway bridge server script.

## Default Flow

1. Use `references/bridge-api.md` if bridge state or API execution is uncertain.
2. Use `references/design-standards.md` before substantial schematic work.
3. Use `references/parts-strategy.md` when choosing real library parts.
4. Use `references/circuit-blocks.md` for common circuit topologies.
5. Use `references/eda-code-patterns.md` while writing `execute_in_eda` code.
6. Use `references/pcb-workflow.md` for PCB/layout tasks.
7. Use `references/examples.md` when trigger behavior or task shape is unclear.

## Official API References

The official EasyEDA API bundle is split by purpose instead of stored as one raw nested package.

Use it when:

- A method signature is uncertain.
- An enum/interface/type is needed.
- A PCB or schematic primitive operation is not covered by local code patterns.
- The user asks about EasyEDA extension development.
- The user explicitly wants official API behavior.

Lookup order:

1. `references/easyeda-api-reference/_quick-reference.md`
2. `references/easyeda-api-reference/_index.md`
3. Specific files under `references/easyeda-api-reference/classes/`
4. Specific enum/interface/type files under `references/easyeda-api-reference/enums/`, `interfaces/`, or `types/`
5. Extension and usage guides under `references/easyeda-official-guides/` and `references/easyeda-user-guide/`

Do not load the whole official reference set into context. Search it with `rg` and open only the relevant files.

## Quality Gate

Before final response:

- Correct page/document is active.
- Components were actually placed, not only text.
- Critical nets exist by sampling recent wires with `getState_Net()`.
- Power rails and grounds are labelled.
- IC power pins have nearby decoupling or documented assumptions.
- Connectors expose labelled nets.
- The schematic is zoomed to all primitives.

Final response should include:

- Page name.
- Main blocks created.
- Real parts used or notable substitutions.
- Verification performed.
- Any assumptions or risks that matter electrically.
