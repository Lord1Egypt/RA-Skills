## Description:

FFHub (ffhub.io). Use this skill for ANY FFHub request — reading, creating, and updating data. Whenever a task involves FFHub, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect FFHub action schemas, create FFmpeg transcoding tasks, and check task status and output files through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback directs the agent to run an external installer whose exact effects are unverified.

Mitigation: Review the setup fallback, install the CLI through a separately reviewed process, and require user approval before running an installer.

## Reference(s):

- [FFHub](https://ffhub.io)
- [FFHub API documentation](https://ffhub.io/docs)
- [oo CLI project (referenced by the skill)](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, API Calls, Guidance]

**Output Format:** [oo CLI commands with JSON payloads and FFHub task responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses depend on the action and can include task status, timing, errors, output files, and an execution ID.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
