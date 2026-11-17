## Description:

Operate an IMesh Python mesh for discovering trusted peers, starting a local node, calling remote skills, managing identities, and checking mesh health.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samajesteduroyaume](https://clawhub.ai/user/samajesteduroyaume)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to start and administer a local IMesh node, discover trusted peers, invoke remote skills, and check gateway health.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exposing skill execution endpoints without authentication can permit unintended use.

Mitigation: Keep the gateway bound to 127.0.0.1 for testing, set a strong OPENCLAW_PSK, and enable OPENCLAW_AUTH_REQUIRED=true before exposing execution endpoints beyond a private single-user local environment.

## Reference(s):

- [IMesh source at the imported revision](https://github.com/samajesteduroyaume/IMesh/tree/main/skills/imesh)
- [IMesh on ClawHub](https://clawhub.ai/samajesteduroyaume/skills/imesh)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
