## Description:

Auto-generate electrical CAD drawings from survey data and auto-audit against power codes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[powerzzjohn](https://clawhub.ai/user/powerzzjohn)

### License/Terms of Use:

MIT-0

## Use Case:

Electrical designers and engineering teams use this skill to turn survey data, sketches, or project briefs into draft 10kV-and-below power distribution CAD packages and preliminary audit reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automated electrical code audit is underimplemented and can falsely pass a safety-relevant design.

Mitigation: Do not rely on the audit as an authoritative compliance check; require independent engineering review for all generated designs.

Risk: A transformer-capacity logic error is identified in the security guidance.

Mitigation: Fix and retest the transformer-capacity rule before using the skill for design approval or compliance workflows.

Risk: The end-to-end workflow and dependency versions are not fully reliable for unattended installation.

Mitigation: Document the complete workflow, pin dependencies, and review the skill before installation or operational use.

## Reference(s):

- [Drawing Symbols](references/drawing_symbols.md)
- [ClawHub skill page](https://clawhub.ai/powerzzjohn/skills/power-cad-drafter)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands, plus generated DXF, JSON, CSV, and Markdown files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ezdxf and pyyaml; generated electrical designs and audit results require independent engineering review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
