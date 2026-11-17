## Description:

Use this skill for Writer requests involving searching and reading data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Writer users use the connected OOMOL account to generate Writer chat completions and list available models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs an unverified CLI installer.

Mitigation: Review the installer and use a verified CLI release before execution.

Risk: The CLI's automatic skill synchronization can change agent skills beyond this Writer integration.

Mitigation: Check the automatic synchronization behavior and limit it if those changes are not intended.

Risk: Writer prompts pass through OOMOL.

Mitigation: Review OOMOL's data handling and avoid sending sensitive prompts unless approved.

## Reference(s):

- [Writer](https://writer.com)
- [Writer API: List Models](https://dev.writer.com/api-reference/completion-api/list-models)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, Text, Guidance]

**Output Format:** [JSON request payloads and Writer text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses depend on the selected Writer action and model.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
