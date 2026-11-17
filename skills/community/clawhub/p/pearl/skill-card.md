## Description:

Pearl lets agents set up and use a Pearl wallet to check balances, view transactions, and call Pearl-powered paid skills with user-controlled charge approvals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[misteeka](https://clawhub.ai/user/misteeka)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Pearl to connect a wallet once, inspect spending state, and allow Pearl-powered agent skills to request paid service calls subject to user approvals and spending limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pearl stores reusable tokens locally in ~/.pearl/config.json.

Mitigation: Treat ~/.pearl/config.json as a credential file, keep it user-readable only, and install Pearl only on machines where local account access is trusted.

Risk: Pearl-powered skills can send a limited reusable skill token to third-party HTTPS provider servers.

Mitigation: Use Pearl only with trusted skills and providers, review approval requests, and monitor Pearl transactions after use.

Risk: Approved providers may create charges that settle automatically within configured spending limits.

Mitigation: Set strict per-charge and daily spending limits and revisit provider approvals when a paid skill is no longer needed.

## Reference(s):

- [Pearl homepage](https://pearlcash.ai)
- [ClawHub Pearl listing](https://clawhub.ai/misteeka/skills/pearl)
- [ClawHub publisher profile](https://clawhub.ai/user/misteeka)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, API Calls, Guidance]

**Output Format:** [Plain text and command output from Node.js scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and reads local Pearl configuration and pending-charge files under ~/.pearl during setup and paid-skill approval flows.]

## Skill Version(s):

0.0.14 (source: server release evidence and _meta.json; package.json reports 0.0.15)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
