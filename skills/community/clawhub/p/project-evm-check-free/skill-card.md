## Description:

Checks project earned value management worksheets locally by recalculating CV, SV, CPI, SPI, totals, duplicate work packages, and blanks, with findings tied to source line numbers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Project managers, PMO staff, and finance or cost analysts use this skill to check earned value worksheet arithmetic before monthly progress and cost reporting. It recalculates stated CV, SV, CPI, SPI, totals, duplicate work packages, and blank or placeholder fields from pasted or JSON-provided table text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The free version only executes the checks it lists and omits several EVM validations such as qualitative CPI/SPI consistency, negative PV/EV/AC detection, EAC and ETC checks, and BAC less than EV checks.

Mitigation: Review the reported checks_withheld and run separate manual or full-version checks when those omitted validations matter.

Risk: Arithmetic results can be mistaken for broader project management assurance.

Mitigation: Use the output as worksheet arithmetic evidence only, and separately validate PV/EV measurement basis, project scope, schedule judgment, and budget decisions.

Risk: Missing headers, blank cells, placeholder values, or insufficient pasted table text prevent reliable conclusions.

Mitigation: Provide table text with recognizable 工作包, PV, EV, AC, CV, SV, CPI, and SPI headers and review any missing-field guidance before relying on results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/project-evm-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)
- [Bundled sample input](artifact/templates/sample.json)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Human-readable console text or JSON containing findings, summary values, executed checks, withheld checks, and insufficient-input details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source line numbers; insufficient input returns missing requirements instead of a pass or fail conclusion.]

## Skill Version(s):

1.0.30 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
