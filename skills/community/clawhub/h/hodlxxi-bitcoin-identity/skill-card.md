## Description: <br>
Read-only-by-default integration guide for HODLXXI / UBID Bitcoin-native identity discovery, OAuth2/OIDC metadata, LNURL-Auth boundaries, JWT verification guidance, and explicit operator-approved agent handoff. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hodlxxi](https://clawhub.ai/user/hodlxxi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to understand and integrate HODLXXI / UBID as a Bitcoin-native identity provider. It supports public discovery, OAuth2/OIDC metadata review, LNURL-Auth boundaries, JWT verification guidance, and operator-approved agent handoff planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OAuth registration, token exchange, wallet login, agent job submission, or Lightning payment actions could expose credentials, identity claims, or funds if performed automatically. <br>
Mitigation: Keep the skill read-only by default and require explicit operator approval for the exact endpoint, payload, scopes, and payment impact before any sensitive or privileged action. <br>
Risk: Identity tokens can be trusted incorrectly if JWT validation is incomplete or uses stale discovery metadata. <br>
Mitigation: Verify issuer, audience, expiration, expected algorithm, key id, signature, and current JWKS before trusting claims. <br>
Risk: Recurring polling or heartbeat behavior can create unwanted persistence or repeated network activity. <br>
Mitigation: Leave heartbeat and polling disabled unless the operator explicitly configures the cadence, destination, and stop condition. <br>


## Reference(s): <br>
- [HODLXXI / UBID homepage](https://github.com/hodlxxi/Universal-Bitcoin-Identity-Layer) <br>
- [ClawHub skill page](https://clawhub.ai/hodlxxi/hodlxxi-bitcoin-identity) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance describing public endpoints, identity-flow boundaries, JWT verification checks, and approval requirements] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only by default; public GET discovery is allowed, while token exchange, OAuth client registration, wallet login, agent job submission, Lightning invoice handling, shell execution, dependency installation, filesystem writes, and recurring polling require explicit operator approval.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
