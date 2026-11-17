## Description:

Operate Postman through your OOMOL-connected account to read and manage Postman resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to inspect Postman action schemas and manage Postman workspaces, collections, APIs, and related resources through the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructs users to run an unverified remote installer, and the hosted connector implementation was not verified.

Mitigation: Use a separately approved CLI release with verified integrity and inspect or disable automatic skill synchronization.

Risk: Postman actions include changes and deletions that can affect account data.

Mitigation: Connect only the Postman account and permissions needed, and require explicit user approval for writes and deletions.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Postman skill on ClawHub](https://clawhub.ai/oomol/skills/oo-postman)
- [OOMOL publisher profile](https://clawhub.ai/user/oomol)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, API responses, Guidance]

**Output Format:** [Shell commands with JSON payloads and structured Postman responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, update, or delete Postman resources when the user approves the action.]

## Skill Version(s):

1.0.6 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
