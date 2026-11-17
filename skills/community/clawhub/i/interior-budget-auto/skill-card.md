## Description:

根据DXF户型图和设计师历史报价库生成家装或工装预算Excel，并尽量保留本地预算模板格式。

This skill is ready for commercial/non-commercial use.

## Publisher:

[137984917-cyber](https://clawhub.ai/user/137984917-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

Interior designers and renovation teams use this skill to turn exported DXF floor plans and a local historical pricing library into an editable Excel budget draft for residential or commercial interior projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script writes an Excel workbook to the user-provided output path and may overwrite an existing workbook.

Mitigation: Use a non-critical output filename or back up any existing workbook before running the script.

Risk: The script depends on a local pricing-library path that may not exist on another machine.

Mitigation: Adjust the pricing-library path for the local environment before use.

Risk: Budget quantities and prices are draft estimates derived from DXF text and a local pricing library.

Mitigation: Review and adjust quantities, pricing, and line items before sharing the budget with customers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/137984917-cyber/skills/interior-budget-auto)
- [Artifact skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, shell commands, code, configuration, guidance]

**Output Format:** [Markdown guidance with Python command examples and generated Excel workbook output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local DXF file, a local pricing-library JSON file, and Python dependencies including openpyxl and ezdxf.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
