## Description:

Supports a Persian-language personal research lab that evaluates evidence about success, designs small experiments, and updates a living model of what improves the user's outcomes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ehsanghaffar](https://clawhub.ai/user/ehsanghaffar)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals use this skill to research questions about success, test personal hypotheses, and maintain a Persian-language research log and evolving model of their findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent sessions can update personal research logs and model files.

Mitigation: Review the storage location and file changes before allowing updates; keep copies of important records.

Risk: An installer may fetch skill content from a source that changes over time.

Mitigation: Use the manual copy/install path or pin the installer source for tighter supply-chain control.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/ehsanghaffar/skills/persian-success-lab)
- [Source registry](references/source-registry.md)
- [Record schemas](references/record-schemas.md)
- [Success model and review cadence](references/success-model.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Files]

**Output Format:** [Persian Markdown with structured research summaries, experiment records, and model updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Research and experiment logs remain separate from the living model; updated records can be provided for manual saving when persistent storage is unavailable.]

## Skill Version(s):

0.1.1 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
