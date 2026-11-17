## Description:

Provides process-industry teams with read-first HART-IP, OPC UA, and Modbus access plus cross-protocol diagnostics for instrumentation, downtime, data quality, and OEE.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Process control and reliability engineers use it to inspect instrumentation and control-system data, triage process issues, and prepare evidence-based diagnostics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Heuristic tag suggestions or diagnostic findings could be treated as confirmed plant facts.

Mitigation: Confirm tag roles and diagnostic findings against site data and operator knowledge before acting; use diagnostic results as triage evidence.

Risk: The optional Sparkplug publishing path can send operational messages.

Mitigation: Require site authorization and the documented MOC controls before publishing, including dry-run review, undo state, and named dual confirmation.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/zw008/skills/iaiops-process)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Configuration, Shell commands, Files]

**Output Format:** [Structured text and data, including readings, diagnostic summaries, Markdown, and configuration drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include numeric evidence, source references, uncertainty states, and warnings.]

## Skill Version(s):

0.34.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
