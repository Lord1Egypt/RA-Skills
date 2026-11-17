## Description:

Passo enables secure remote access to a browser on a server so a trusted user can complete manual web tasks such as logins, two-factor authentication, captchas, and other browser actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[felipegoulu](https://clawhub.ai/user/felipegoulu)

### License/Terms of Use:


## Use Case:

Agents and developers use Passo when a remote human needs temporary access to a server-hosted browser to complete manual actions the agent cannot handle alone. Typical tasks include account sign-ins, two-factor authentication, captchas, and other browser workflows requiring trusted human input.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an unverified remote installer.

Mitigation: Download and inspect a pinned installer with a published checksum before installation, and do not run it as root unless the installer has been verified.

Risk: Live remote browser sessions can expose tokens, account data, recovery flows, and sensitive manual login steps.

Mitigation: Use an isolated host or disposable browser profile, share access only with trusted users, and avoid highly sensitive accounts unless the remote-access service is fully trusted.

Risk: A shared browser access URL can allow manual control of a server-hosted browser during the session.

Mitigation: Restrict access to the intended email, stop the tunnel after the task is complete, and check session status before and after sharing access.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/felipegoulu/skills/passo)
- [Passo Website](https://getpasso.app)
- [Passo Documentation](https://getpasso.app/docs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and placeholder values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include an access URL, an authorized email, command-line status guidance, and installation or subscription notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
