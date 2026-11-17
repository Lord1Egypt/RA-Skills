## Description:

Helps an agent create, delete, restore, or purge Kiipu posts, manage authentication, and check local setup through the Kiipu CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mycreat](https://clawhub.ai/user/mycreat)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to operate Kiipu posts and CLI setup from Claude Code while relying on the local Kiipu CLI for authentication, environment handling, and execution results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A purge command permanently removes a Kiipu post.

Mitigation: Verify the exact post ID before running delete, restore, or purge, and treat purge as irreversible.

Risk: The skill depends on installing and running a global npm CLI package.

Mitigation: Install only from a trusted Kiipu CLI package source, and use a pinned version or isolated install when stricter supply-chain control is needed.

Risk: Post-management commands can affect the wrong content when an ID is missing or incorrect.

Mitigation: Require an explicit post ID for delete, restore, and purge actions and return the CLI result accurately.

## Reference(s):

- [Kiipu Skill on ClawHub](https://clawhub.ai/mycreat/skills/kiipu)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report Kiipu CLI results and request explicit post IDs for delete, restore, or purge actions.]

## Skill Version(s):

0.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
