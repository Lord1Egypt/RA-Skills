## Description:

Gets threat intelligence for security operations and automation tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Security analysts and automation engineers use this skill to request threat-intelligence results for indicators, incident details, or other security inputs during operations workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is broadly scoped and unclear about which threat-intelligence script or external service handles submitted security inputs.

Mitigation: Review the implementation and provider before installing, especially where indicators, internal domains, incident details, or artifacts may be sent.

Risk: The documented workflow requires an INTEL_API_KEY credential.

Mitigation: Store the API key in an approved secret-management mechanism and avoid committing it to skill files, logs, shell history, or shared configuration.

Risk: The artifact references scripts/threat_intelligence.py, but that script is not included in the provided artifact.

Mitigation: Confirm the referenced script and its data-handling behavior before executing the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jpengcheng523-netizen/skills/jpeng-threat-intelligence)
- [ClawHub Publisher Profile](https://clawhub.ai/user/jpengcheng523-netizen)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands and JSON output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documents use of INTEL_API_KEY and JSON result output.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
