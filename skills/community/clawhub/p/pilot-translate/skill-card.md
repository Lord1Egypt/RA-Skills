## Description:

Auto-translate messages between agents using different languages over the Pilot Protocol network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure Pilot Protocol workflows for cross-language agent communication with external translation tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install guidance includes downloading an external translation executable and moving it system-wide with sudo.

Mitigation: Use a verified, pinned translation tool from a trusted package manager or install without sudo where possible.

Risk: Messages may be translated through third-party services when using external CLI tools or APIs.

Mitigation: Avoid translating confidential messages through third-party services unless approved; prefer local or self-hosted translators for sensitive data.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)
- [ClawHub skill listing](https://clawhub.ai/teoslayer/skills/pilot-translate)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the pilotctl binary on PATH, a running Pilot Protocol daemon, and a separately installed translation tool.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
