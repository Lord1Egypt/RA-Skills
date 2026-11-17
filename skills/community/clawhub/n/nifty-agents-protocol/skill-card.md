## Description:

A cryptographic protocol for AI agents to mint, sign, verify, and transfer SVG digital assets without a blockchain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[obekt](https://clawhub.ai/user/obekt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add TypeScript workflows for signing SVG assets, verifying embedded provenance, and transferring ownership between did:key identities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Divergent valid transfer chains can create ownership conflicts when there is no authoritative registry, marketplace log, or consensus layer.

Mitigation: Use the protocol only for experiments or low-value provenance unless authoritative transfer ordering is added; do not resolve ownership by longest chain or latest timestamp alone.

Risk: Generated secret keys control asset transfers, and the simulation vault pattern stores keys as local files.

Mitigation: Treat generated keys as credentials and use production secret management instead of the simulation vault for real deployments.

Risk: The optional verification server may expose SVG verification over HTTP without authentication or rate limits.

Mitigation: Bind the verifier to localhost unless exposure is intentional, and add authentication, rate limits, and dependency updates or pinning before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/obekt/skills/nifty-agents-protocol)
- [Project homepage](https://github.com/obekt/niftyagents)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with TypeScript and shell command snippets; generated protocol operations can produce signed SVG files and JSON verification results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API-key environment variables are required by the artifact metadata.]

## Skill Version(s):

1.0.3 (source: server release, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
