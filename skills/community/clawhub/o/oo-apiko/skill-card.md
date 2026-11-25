## Description:

APIKO (apiko.app). Use this skill for ANY APIKO request — searching and reading data. Whenever a task involves APIKO, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers can use this skill to inspect APIKO's available model IDs and request chat completions through their connected APIKO account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions use a remote installer whose downloaded contents were unavailable to the security scan.

Mitigation: Review the installer before running it; the security scan was partial.

Risk: Authentication and billed inference actions are not clearly tied to the stated search and read purpose.

Mitigation: Confirm the connected account and expected charges before requesting a chat completion.

## Reference(s):

- [APIKO documentation](https://apiko.app/docs/introduction)
- [APIKO homepage](https://apiko.app)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [APIKO ClawHub release](https://clawhub.ai/oomol/skills/oo-apiko)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Text]

**Output Format:** [Markdown guidance with shell commands and JSON inputs; API responses may contain JSON or generated text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chat completion requests are billed.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
