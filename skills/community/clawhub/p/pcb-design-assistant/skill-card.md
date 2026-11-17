## Description: <br>
PCB设计助手 is an EasyEDA/JLCPCB-focused PCB design copilot that helps agents select real components, organize schematics, interpret DRC issues, and prepare production handoff files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, hardware engineers, makers, and small hardware teams use this skill to drive EasyEDA/JLCPCB PCB workflows, resolve schematic and DRC issues, and produce BOM, CPL, Gerber, assembly, and design-note deliverables for fabrication review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated PCB manufacturing packages may contain schematic, footprint, DRC/ERC, BOM availability, electrical safety, or cost-sensitive issues. <br>
Mitigation: Manually review schematics, footprints, DRC/ERC results, BOM availability, electrical safety, and cost choices before fabrication or ordering. <br>
Risk: The skill can guide agents through EasyEDA operations and optional local command execution. <br>
Mitigation: Install only when the agent is expected to operate PCB/EasyEDA workflows, and review proposed commands or generated bridge code before execution. <br>
Risk: Component inventory and substitution guidance can become stale before a board is ordered. <br>
Mitigation: Verify selected JLCPCB/EasyEDA components, stock status, packages, and substitutes during final BOM review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/pcb-design-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline code or shell commands and generated PCB handoff file specifications] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require EasyEDA access, optional MCP or bridge tooling, and manual fabrication review before ordering.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
