## Description:

Use DocuSeal to list and retrieve templates or create signature requests through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People who manage DocuSeal workflows can use this skill to list templates, retrieve a template, and create signature requests from existing templates. It is intended for use with an OOMOL account connected to DocuSeal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An ordinary request may trigger remote software installation without a separate approval step.

Mitigation: Review and install a verified oo release before enabling the skill, and check automatic agent-skill installation and synchronization settings.

Risk: The skill can access connected DocuSeal data and create signature requests.

Mitigation: Keep signature requests confirmation-gated and review the action schema and payload before creating a request.

## Reference(s):

- [DocuSeal skill release](https://clawhub.ai/oomol/skills/oo-docuseal)
- [DocuSeal](https://www.docuseal.com)
- [DocuSeal API documentation](https://www.docuseal.com/docs/api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON data, Guidance]

**Output Format:** [Markdown instructions with shell commands and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports read actions and signature-request creation; signature requests should remain confirmation-gated.]

## Skill Version(s):

1.0.6 (source: release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
