## Description:

letsping routes high-risk OpenClaw agent actions through human approval before destructive, financial, social, or infrastructure changes proceed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cordialabsio](https://clawhub.ai/user/cordialabsio)

### License/Terms of Use:


## Use Case:

Developers and operators using OpenClaw use this skill to require human approval before an agent performs high-risk tool calls and to resume only with an approved or patched payload.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an unpinned external runtime.

Mitigation: Install a pinned, audited package version or commit before enabling the skill.

Risk: LETSPING_API_KEY is a sensitive runtime credential.

Mitigation: Use a dedicated scoped agent key, keep it out of source control, and revoke it if compromised.

Risk: The suggested agent policy grants broad autonomous read authority without explicit sensitive-data limits.

Mitigation: Add approval rules for reading or transmitting secrets, private logs, credentials, browser or session data, and agent memory.

Risk: Model drift or prompt injection can cause an agent to skip the approval call.

Mitigation: Test in a sandbox, use strong models, and tighten prompt examples for each high-risk category.

## Reference(s):

- [Artifact README](artifact/README.md)
- [OpenClaw runtime repository](https://github.com/CordiaLabs/openclaw-skill)
- [LetsPing OpenClaw pairing](https://letsping.co/openclaw/pair)
- [LetsPing](https://letsping.co)
- [ClawHub skill page](https://clawhub.ai/cordialabsio/skills/letsping)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell command and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides approval-flow guidance for high-risk OpenClaw tool calls and expects LETSPING_API_KEY at runtime.]

## Skill Version(s):

0.3.5 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
