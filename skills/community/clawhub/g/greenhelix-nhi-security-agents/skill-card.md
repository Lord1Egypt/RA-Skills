## Description:

A guide for securing non-human identities in AI agent deployments, including lifecycle management, credential rotation, workload identity federation, machine-to-machine authentication, governance tooling, zero trust, and compliance patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security engineers, and platform teams use this skill as guidance for designing, reviewing, and hardening non-human identity controls for AI agent systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guide references sensitive credentials even though it is primarily educational.

Mitigation: Do not provide production Stripe, signing, Vault, OAuth, or cloud credentials merely to read or evaluate the guide.

Risk: Runnable examples include broad secret and cloud-token access patterns.

Mitigation: Use sandbox credentials, restrict scan paths and environment-variable access, and add allowlists around cloud token audiences and identity operations before adapting examples.

Risk: Example code may expose credential material through copied logging or debugging behavior.

Mitigation: Review copied code before execution and avoid logging token fragments or secret values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mirni/skills/greenhelix-nhi-security-agents)
- [Publisher profile](https://clawhub.ai/user/mirni)
- [GreenHelix sandbox](https://sandbox.greenhelix.net)
- [Agent Production Hardening Guide](https://clawhub.ai/skills/greenhelix-agent-production-hardening)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with illustrative code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Educational guide content; artifact metadata marks it non-executable with no install step.]

## Skill Version(s):

1.3.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
