## Description:

Confidential real-world-asset (RWA) portfolio agent built on MuHaven's Fhenix-CoFHE-encrypted token primitives for reading encrypted balances and staging buy or yield-claim intents for human confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hastodev](https://clawhub.ai/user/hastodev)

### License/Terms of Use:

MIT-0

## Use Case:

External MuHaven users use this skill to inspect encrypted RWA portfolio information, review yield and compliance context, and prepare buy, claim, or pause requests that require human confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security review flags user-level execution exposure in the documented host_native setup.

Mitigation: Install only with exact pinned runtime and CLI versions, and prefer an isolated OS account or container.

Risk: The security summary says the financial authority is paired with installation and runtime documentation that weakens or overstates security boundaries.

Mitigation: Use read-only mode unless intentionally staging buy, claim, or pause actions, and review the runtime security posture before enabling state-changing tools.

## Reference(s):

- [MuHaven homepage](https://muhaven.app)
- [ClawHub skill page](https://clawhub.ai/hastodev/skills/muhaven-rwa-skill-rehearsal)
- [OpenClaw skill documentation](https://github.com/hasToDev/muhaven/tree/master/packages/openclaw-skill)
- [MuHaven support](https://github.com/hasToDev/muhaven/issues)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown and structured tool-call results with confirmation instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [State-mutating actions are staged for human confirmation; read-only mode limits output to portfolio and policy inspection.]

## Skill Version(s):

0.1.0-rc.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
