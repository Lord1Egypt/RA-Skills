## Description:

Generate breadboard circuit mockups and visual diagrams using HTML5 Canvas drawing techniques.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhauga](https://clawhub.ai/user/jhauga)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, educators, and electronics hobbyists use this skill to create breadboard layouts and visual diagrams for retro computing circuits, 555 timer projects, EEPROM/SRAM designs, LCD interfaces, and 6502-based builds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes optional root-level software installation and chip-writing guidance that is broader and riskier than simple circuit mockups.

Mitigation: Treat minipro and T48 programmer sections as privileged manual operations; prefer trusted package-manager installs, avoid unpinned source builds with sudo, verify upstream releases, and back up chips before write or erase operations.

Risk: Physical circuit builds can be damaged by incorrect low-voltage wiring or component orientation.

Mitigation: Double-check low-voltage circuit safety, power rails, component polarity, and chip pin orientation before powering physical builds.

## Reference(s):

- [Legacy Circuit Mockups Skill](https://clawhub.ai/jhauga/skills/legacy-circuit-mockups)
- [AT28C256 256K (32K x 8) Parallel EEPROM Specification](references/28256-eeprom.md)
- [555](references/555.md)
- [MOS Technology 6502 Microprocessor Specification](references/6502.md)
- [MOS Technology 6522 Versatile Interface Adapter (VIA)](references/6522.md)
- [AS6C62256 32K x 8 Low-Power CMOS SRAM Specification](references/6C62256.md)
- [7400-Series Logic ICs Specification](references/7400-series.md)
- [6502 SBC Assembly Compilation & ROM Build Specification](references/assembly-compiler.md)
- [6502 Assembly Language with AT28C256 EEPROM](references/assembly-language.md)
- [Basic Electronic Components](references/basic-electronic-components.md)
- [Solderless Breadboard](references/breadboard.md)
- [Common Breadboard Electronic Components](references/common-breadboard-components.md)
- [Connecting Electronic Components](references/connecting-electronic-components.md)
- [AT28C256 EEPROM Emulation Specification](references/emulator-28256-eeprom.md)
- [6502 CPU Emulation Specification](references/emulator-6502.md)
- [6522 VIA (Versatile Interface Adapter) Emulation Specification](references/emulator-6522.md)
- [AS6C62256 (32K x 8 SRAM) Emulation Specification](references/emulator-6C62256.md)
- [DFRobot FIT0127 LCD Character Display Emulation Specification](references/emulator-lcd.md)
- [DFRobot FIT0127 LCD Character Display Specification](references/lcd.md)
- [minipro Chip Programming Utility Specification](references/minipro.md)
- [T48 Universal EEPROM / Flash Programmer Specification](references/t48eeprom-programmer.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with JavaScript and HTML5 Canvas code examples, circuit layout guidance, component tables, and wiring steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include visual mockup instructions, pinout references, wiring color conventions, and manual hardware programming guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
