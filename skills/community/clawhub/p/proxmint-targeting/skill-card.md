## Description:

Build Proxmint proxy usernames for location targeting and sticky sessions. Use when the user needs exits in a specific country, state, city, ZIP code or ISP (ASN), wants to exclude countries, needs one IP held through a login or multi-step flow, or wants each worker, account or browser profile on its own IP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prian3003](https://clawhub.ai/user/prian3003)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build Proxmint proxy usernames for geographic or ISP targeting and sticky sessions, then place them in code or proxy tools while keeping credentials private.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External IP verification services receive the queried IP address and connection metadata.

Mitigation: Ask to skip external verification when sharing this information is unsuitable.

Risk: Proxy credentials could be exposed when constructing usernames or proxy URLs.

Mitigation: Keep proxy credentials private, read the login from the environment where practical, and never include the password in examples.

Risk: Narrow location targeting can consume additional bandwidth credits.

Mitigation: Account for the disclosed targeting cost before running heavy city, ZIP, or ISP-targeted traffic.

## Reference(s):

- [Proxmint documentation](https://proxmint.com/docs)
- [Proxmint pricing](https://proxmint.com/pricing)
- [Proxmint status](https://proxmint.com/status)
- [ClawHub skill page](https://clawhub.ai/prian3003/skills/proxmint-targeting)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with proxy username strings and inline code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples use a placeholder login; the skill says never to include a password.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
