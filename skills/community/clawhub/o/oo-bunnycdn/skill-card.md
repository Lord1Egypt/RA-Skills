## Description:

Use the OOMOL-connected oo CLI for BunnyCDN Pull Zone lookups and cache purges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and BunnyCDN account operators can inspect Pull Zones and request cache purges through an OOMOL-connected account. The skill requires approval of the target before a destructive cache purge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup directs the agent to execute unverified remote code without separate approval.

Mitigation: Install a pinned, independently verified CLI release yourself and review its automatic skill installation behavior.

Risk: Connecting BunnyCDN entrusts OOMOL with provider access and request data.

Mitigation: Review the connection and proceed only if you are comfortable entrusting OOMOL with that access and data.

Risk: Purging a Pull Zone cache is destructive.

Mitigation: Require explicit approval of the target before purging.

## Reference(s):

- [BunnyCDN](https://bunny.net/)
- [BunnyCDN documentation](https://bunny.net/docs)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [BunnyCDN skill on ClawHub](https://clawhub.ai/oomol/skills/oo-bunnycdn)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON action results and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available operations include Pull Zone reads and cache purges; cache purges are destructive.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
