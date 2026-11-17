## Description:

Inspect PhantomBuster agents, automations, launches, and workflow data via the PhantomBuster API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect PhantomBuster account activity, review launch output, and manage automation workflows through ClawLink-backed PhantomBuster API tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated PhantomBuster write, delete, or launch actions can affect the connected account and third-party systems.

Mitigation: Review previews carefully and require explicit user confirmation before any write, delete, or automation launch.

Risk: The skill depends on a ClawLink plugin connection that makes authenticated PhantomBuster API calls.

Mitigation: Confirm the ClawLink plugin source is trusted and verify the PhantomBuster connection before using account data or automation tools.

Risk: Automation launches may consume PhantomBuster or third-party service rate limits.

Mitigation: Confirm the target automation and intended effect before launch, and use backoff when rate limits are encountered.

## Reference(s):

- [PhantomBuster API Documentation](https://hub.phantombuster.com/reference)
- [PhantomBuster](https://phantombuster.com/)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [PhantomBuster Automation Skill Page](https://clawhub.ai/hith3sh/skills/phantombuster-automation)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON tool parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call authenticated PhantomBuster tools through ClawLink after connection setup and user confirmation for write actions.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
