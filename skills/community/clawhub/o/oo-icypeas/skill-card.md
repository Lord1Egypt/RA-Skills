## Description:

Icypeas (icypeas.com). Use this skill for ANY Icypeas request — reading, creating, and updating data. Whenever a task involves Icypeas, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to retrieve Icypeas search results and subscription details, find professional profiles by email, and submit email discovery, verification, or domain-scan requests through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required CLI may change other agent skills during installation or startup synchronization, a broader effect not fully explained in the skill.

Mitigation: Review the CLI's additional skill installation and verify the CLI release. For normal CLI calls, set OO_SKILLS_SYNC_DISABLED=1; review the fallback installer separately before using it.

## Reference(s):

- [Icypeas homepage](https://www.icypeas.com)
- [Icypeas API documentation](https://api-doc.icypeas.com/getting-started)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance, Shell commands]

**Output Format:** [JSON action results with concise text summaries and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected Icypeas action; state-changing actions require user confirmation.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
