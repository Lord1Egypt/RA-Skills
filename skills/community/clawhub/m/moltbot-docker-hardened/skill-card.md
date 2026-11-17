## Description:

Enables the bot to manage Docker containers, images, and stacks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to ask an agent for Docker container, image, stack, log, inspection, build, push, and cleanup assistance while applying confirmation and redaction guardrails around high-risk Docker operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Docker commands can modify or delete containers, images, networks, volumes, and stacks.

Mitigation: Review confirmation prompts carefully before destructive operations, including rm, rmi, system prune, volume or network removal, bulk stop or kill, and commands using force flags.

Risk: Docker logs, inspect output, environment variables, and image layers may contain credentials or other sensitive data.

Mitigation: Keep Docker output local, redact secret values in responses, verify secret presence without printing values, and confirm registry targets before any push.

Risk: Pulling or building untrusted images and Dockerfiles can introduce supply-chain or remote-code-execution risk.

Mitigation: Confirm unverified image publishers and third-party registries before pulls, and review Dockerfiles for remote script execution, untrusted base images, and baked-in secrets before builds.

Risk: docker exec can grant broad access inside running containers, including sensitive services and credentials.

Mitigation: Require confirmation before sensitive exec commands, shell spawning, or state-changing commands, and prefer scoped diagnostic commands when possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/skills/moltbot-docker-hardened)
- [Faberlens safety evaluation](https://faberlens.ai/explore/moltbot-docker)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with Docker CLI commands, summaries, confirmations, and redacted diagnostic guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request user confirmation before destructive, publishing, untrusted image, sensitive exec, or data-access operations; summarizes lengthy Docker output.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
