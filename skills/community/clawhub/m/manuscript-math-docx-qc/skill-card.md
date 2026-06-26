## Description: <br>
Portable agent skill/playbook for OpenClaw, Hermes, Claude, Codex, and other agents revising scientific manuscripts that will be exported to DOCX/PDF, especially when mathematical formulas, subscripted variables, tables, figures, Word rendering, Pandoc conversion, LibreOffice PDF checks, or submission-package visual QC may fail. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xutaoguo55](https://clawhub.ai/user/xutaoguo55) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, research agents, and manuscript authors use this skill to check scientific manuscript sources and generated DOCX/PDF submission artifacts for math rendering, figure layout, table overflow, and stale upload-package files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local conversion and cleanup commands may modify generated manuscript artifacts or remove rendered page images. <br>
Mitigation: Review command paths before execution and keep source manuscripts and required build outputs under version control or backed up. <br>
Risk: Upload package synchronization can copy stale or unintended files if paths are wrong. <br>
Mitigation: Compare file sizes and timestamps, rebuild the final archive, and validate it with unzip before submission. <br>
Risk: Formula, figure, or table changes suggested by the skill can affect scientific presentation. <br>
Mitigation: Inspect rebuilt DOCX/PDF pages visually and have domain owners review substantive manuscript edits. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xutaoguo55/manuscript-math-docx-qc) <br>
- [SKILL.md](SKILL.md) <br>
- [README.md](README.md) <br>
- [AGENTS.md](AGENTS.md) <br>
- [Minimal QC Example](examples/minimal/qc_commands.sh) <br>
- [Improved QC Example](examples/improved/qc_commands.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and file-path guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include corrected source edits, rebuilt DOCX/PDF paths, visual QC notes, validation command results, and upload package checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
