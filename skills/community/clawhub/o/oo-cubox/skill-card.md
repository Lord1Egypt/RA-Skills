## Description:

Cubox (cubox.pro). Use this skill for ANY Cubox request — reading, creating, and updating data. Whenever a task involves Cubox, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using an OOMOL-connected Cubox account can ask an agent to save a web page to Cubox. The skill guides the agent to inspect the action schema, submit a matching request, and obtain approval before saving content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup offers remote CLI installers that can run without separate user approval.

Mitigation: Preinstall a trusted, version-pinned CLI through an approved process, and require separate approval for software installation.

Risk: Saving content changes the connected Cubox account, and requests pass through OOMOL.

Mitigation: Review the connected account's permissions and approve each write payload before running it.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Cubox](https://cubox.pro)
- [Cubox save API documentation](https://help.cubox.pro/save/89d3/)
- [oo CLI install guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Shell commands with JSON request payloads and connector response data, plus Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Connector response fields depend on the selected Cubox action.]

## Skill Version(s):

1.0.4 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
