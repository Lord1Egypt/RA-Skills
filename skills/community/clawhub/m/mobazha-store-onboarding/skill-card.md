## Description:

Complete the first-time setup wizard for a new Mobazha store. Use after deployment to configure admin password, store name, currencies, and profile.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengzie](https://clawhub.ai/user/fengzie)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and store operators use this skill to complete first-time Mobazha store onboarding across SaaS, VPS standalone, and local deployments. It guides setup of admin access, store profile, currency, visibility, and related post-onboarding tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles store admin passwords and bearer tokens during setup.

Mitigation: Ask for explicit consent before credential handling, avoid logging or storing secrets, and limit credentials to the immediate setup step.

Risk: Some setup paths use HTTP or local/LAN access, which can expose credentials if used outside trusted environments.

Mitigation: Prefer HTTPS or a trusted tunnel for non-localhost admin and MCP access, and isolate local services from untrusted networks.

Risk: Password reset guidance includes deleting the auth database and restarting the service.

Mitigation: Back up the datastore, isolate the service from LAN or Internet access, and run reset commands only when intentional and immediately followed by password setup.

## Reference(s):

- [Mobazha Access Modes](references/access-modes.md)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration instructions]

**Output Format:** [Markdown with HTTP examples and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user consent before handling admin passwords, bearer tokens, or setup API calls.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
