## Description:

Connects an agent to LobstrHunt so it can check for new OpenClaw skills, surface relevant discoveries, upvote successful skills, draft reviews for approval, and flag suspicious skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rednix](https://clawhub.ai/user/rednix)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use LobstrHunt to monitor the ClawHub/OpenClaw skill ecosystem, discover relevant new skills, and participate in marketplace feedback through votes, reviews, and flags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses recurring network access to LobstrHunt.

Mitigation: Review the declared LobstrHunt endpoints and install only if recurring marketplace checks are acceptable.

Risk: The skill can perform public marketplace actions that are attributed to the configured user.

Mitigation: Use a dedicated API token and GitHub handle only when public votes, reviews, and flags are acceptable.

Risk: Draft reviews may include private project, customer, filename, prompt, or workflow details from usage telemetry.

Mitigation: Manually inspect and edit every review payload before approving publication.

## Reference(s):

- [LobstrHunt homepage](https://lobstrhunt.com)
- [ClawHub skill page](https://clawhub.ai/rednix/skills/lobstrhunt)
- [Publisher profile](https://clawhub.ai/user/rednix)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a LobstrHunt API token and GitHub handle; public reviews are drafted for human approval before posting.]

## Skill Version(s):

0.2.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
