## Description:

Read-only-by-default integration guide for HODLXXI / UBID Bitcoin-native identity discovery, OAuth2/OIDC metadata, LNURL-Auth boundaries, JWT verification guidance, and explicit operator-approved agent handoff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hodlxxi](https://clawhub.ai/user/hodlxxi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to read public HODLXXI identity discovery metadata and explain OAuth/OIDC, LNURL-Auth, JWT verification, agent handoff, and Lightning payment boundaries without taking privileged actions by default.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Identity credentials, bearer tokens, private keys, wallet material, cookies, or environment values could be exposed if an agent treats the skill as permission to handle secrets.

Mitigation: Keep the skill read-only by default and do not request, print, persist, or transmit secrets through the skill.

Risk: OAuth registration, token exchange, LNURL-Auth session creation, agent job submission, or Lightning payment actions could affect identity, execution, or funds.

Mitigation: Require explicit operator approval for the exact destination, payload class, and payment behavior before any sensitive or privileged action.

Risk: JWT identity claims could be trusted incorrectly if token validation is incomplete.

Mitigation: Verify issuer, audience, expiration, signature algorithm, key id, and current JWKS before trusting identity claims.

Risk: Recurring polling or heartbeat behavior could create unintended persistence or beaconing.

Mitigation: Keep heartbeat behavior disabled by default and enable recurring polling only when the operator explicitly configures it.

## Reference(s):

- [Universal Bitcoin Identity Layer](https://github.com/hodlxxi/Universal-Bitcoin-Identity-Layer)
- [HODLXXI public deployment](https://hodlxxi.com)
- [ClawHub skill page](https://clawhub.ai/hodlxxi/skills/hodlxxi-bitcoin-identity)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with endpoint references, boundary checks, and approval requirements.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only by default; sensitive identity, payment, execution, shell, dependency, and filesystem actions require explicit operator approval.]

## Skill Version(s):

0.1.2 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
