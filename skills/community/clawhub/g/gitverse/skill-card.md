## Description:

GitVerse API lets an agent work with GitVerse repositories, issues, and pull requests through CLI commands that return JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[webchi](https://clawhub.ai/user/webchi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to inspect GitVerse repositories, issues, and pull requests, and to create pull requests when repository changes are ready for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A GitVerse token could be sent to an unintended API endpoint if a custom endpoint is configured.

Mitigation: Use a narrowly scoped, revocable GitVerse token and only set GITVERSE_BASE_URL for endpoints you intentionally trust.

Risk: A pull request could be created against the wrong repository or branch if command parameters are incorrect.

Mitigation: Confirm the owner, repository, head branch, base branch, title, and body before executing pull request creation.

Risk: Environment configuration from an untrusted directory can alter token or endpoint settings.

Mitigation: Run the CLI from trusted directories and inspect environment variables before invoking commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/webchi/skills/gitverse)
- [GitVerse API endpoint](https://gitverse.ru/api/v1)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSON from CLI commands, with Markdown guidance for setup and command selection]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a GITVERSE_TOKEN environment variable; command errors are reported to stderr.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
