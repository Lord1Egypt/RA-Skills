## Description:

Use this skill to read, create, update, and delete Moorcheh data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users and developers use this skill to search and retrieve Moorcheh data, or to create namespaces, upload documents, and delete documents. It directs the agent to inspect each action's schema and to obtain confirmation before writes or deletions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: If the oo CLI is missing, setup directs the agent to execute an installer downloaded from the internet.

Mitigation: Install the CLI through a separately approved process with verified provenance, and require approval before executing downloaded installers.

Risk: Moorcheh requests pass through OOMOL, and writes or deletions can change or remove account data.

Mitigation: Account for the OOMOL-mediated connection and retain the skill's confirmation requirements for the exact write or deletion action.

## Reference(s):

- [Moorcheh homepage](https://www.moorcheh.ai)
- [Moorcheh API documentation](https://docs.moorcheh.ai/api-reference/introduction)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Shell commands with JSON input and JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action-specific payloads and results; write and deletion actions require user confirmation.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
