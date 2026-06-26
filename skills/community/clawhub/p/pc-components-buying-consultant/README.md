# PC Components Buying Consultant

> Turns any AI agent into an expert PC build consultant for first-time builders.

## What it does

Guides first-time PC builders through a complete system build decision framework — covering CPU/GPU budget allocation by use case, RAM generation and capacity, PSU wattage calculation with efficiency ratings, CPU cooler TDP matching, motherboard chipset tier selection, storage tier selection, and case airflow/clearance. Works through components in dependency order so every decision is compatible with the ones before it. Delivers a prioritised spec list, a compatibility summary table, and up to 5 real build examples matched to the user's confirmed specs.

## How it works

1. Agent asks targeted, research-backed questions grouped by theme: use case and workloads, display and resolution targets, reused components, physical environment, thermals and noise, storage needs, upgrade path, and regional power standards
2. Determines CPU/GPU budget split by use case archetype (gaming, rendering, streaming, creative, productivity)
3. Works through the component dependency chain in order: CPU platform → GPU VRAM → RAM generation and speed → PSU wattage calculation → cooler TDP matching → motherboard chipset and VRM tier → storage tier → case clearances
4. Flags common first-time builder mistakes proactively (VRM mismatch, DDR generation error, single-stick RAM, undersized PSU, sealed case on high-TDP build, AIO radiator fit)
5. Delivers: Non-negotiable specs → Recommended specs → Optional extras → Compatibility summary table → Spec Summary Card → up to 5 build tier examples

## Requirements

- No external APIs or environment variables required
- No runtime dependencies
- Works with any AI agent that supports SKILL.md (OpenClaw, ClawHub, etc.)
- Pure instruction-based — agent reasoning does the work

## Specs and decisions covered

| Component   | What the skill determines                                                                                 |
| ----------- | --------------------------------------------------------------------------------------------------------- |
| CPU         | Architecture generation, core count, socket, TDP/sustained power draw                                     |
| GPU         | VRAM minimum, API (CUDA/ROCm) requirement, PCIe generation, power connector                               |
| RAM         | DDR generation (DDR4/DDR5), capacity, dual-channel config, speed sweet spot                               |
| PSU         | Calculated wattage (CPU + GPU + system overhead + 20–30% headroom), 80 Plus tier, modularity, form factor |
| CPU Cooler  | TDP headroom, air vs AIO, radiator size, height clearance                                                 |
| Motherboard | Socket, chipset tier, DDR generation, VRM quality, form factor, M.2 slot count                            |
| Storage     | NVMe PCIe Gen (3/4), capacity, secondary drive need                                                       |
| Case        | Form factor, GPU length clearance, cooler height clearance, airflow panel type, radiator mount            |

## Compatibility checks performed

- CPU socket ↔ Motherboard chipset
- RAM generation ↔ Motherboard DDR support
- GPU physical length ↔ Case GPU clearance
- Cooler height ↔ Case cooler clearance
- AIO radiator size ↔ Case radiator mount positions
- PSU form factor ↔ Case PSU bay (ATX vs SFX)
- Estimated system load ↔ PSU wattage with headroom

## Installation

Add via ClawHub or reference the SKILL.md directly in your agent configuration.

## License

MIT

## Homepage

https://github.com/arbazex/personal-tech-buying-consultants/tree/master/pc-components-buying-consultant
