## Description:

Search and read Zorus data through the OOMOL-connected Zorus connector.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People with an installed, signed-in oo CLI and a connected Zorus account can search and read Zorus unblock requests, customers, endpoints, groups, and policies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions use a remote installer whose code has not been verified.

Mitigation: Review the installer and provision a verified oo CLI before use.

Risk: The required CLI can silently install or refresh additional agent skills.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 for CLI invocations if additional skill installation or refresh is not wanted.

Risk: Zorus requests and results pass through OOMOL.

Mitigation: Check organizational data-handling requirements before sending sensitive information through the connector.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [Zorus](https://www.zorustech.com)
- [Zorus API documentation](https://developer.zorustech.com/api/docs/index.html)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Text, Guidance]

**Output Format:** [Shell commands with JSON input and JSON results, plus Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses include Zorus data and execution metadata.]

## Skill Version(s):

1.0.5 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
