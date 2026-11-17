## Description:

Helps agents publish, update, or explain how to publish AI-generated HTML, Markdown, image, or document content to Nishare through its API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[momofa](https://clawhub.ai/user/momofa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to publish generated HTML, Markdown, image, or document content to Nishare, update existing Nishare projects, and return share links with clear API examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents can publish or update user-provided content on an external Nishare service.

Mitigation: Review content before upload and install the skill only when publishing or updating Nishare content is intended.

Risk: Published pages, documents, or images may expose secrets or private data if included in the submitted content.

Mitigation: Remove secrets and private information before sharing content through Nishare.

Risk: API keys may be exposed or overused when authenticated publishing or updates are not required.

Mitigation: Provide Nishare API keys only when account, workspace, or update operations require authentication.

## Reference(s):

- [Nishare API Reference](references/api.md)
- [Source repository](https://github.com/momofa/nishare)
- [ClawHub skill page](https://clawhub.ai/momofa/skills/nishare)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API payload examples and curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Nishare API request details, authentication header guidance, validation rules, and shareUrl response handling.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
