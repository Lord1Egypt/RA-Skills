## Description:

Authenticate to LNURL-auth (LUD-04) services without a wallet, node, or payment. Use when a site provides an lnurl1... challenge for Sign in with Lightning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dyegolara](https://clawhub.ai/user/dyegolara)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to authenticate to Sign in with Lightning services from a provided lnurl1 challenge. It is intended for authentication flows where the decoded service URL and callback can be inspected before submitting the signed challenge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can send login artifacts to insecure, internal, or unexpected callback URLs.

Mitigation: Use only LNURL challenges from trusted services, run with --dry-run --json first, and verify the callback host and scheme before submitting.

Risk: Using --single-key can correlate authentication across service domains.

Mitigation: Avoid --single-key unless cross-domain correlation is intentional and acceptable.

Risk: Running the helper in environments with sensitive internal HTTP services can increase exposure if callback protections are missing.

Mitigation: Avoid those environments until HTTPS, same-origin, redirect, and private-network protections are added.

## Reference(s):

- [LNURL Auth ClawHub skill page](https://clawhub.ai/dyegolara/skills/lnurl-auth)
- [Project homepage](https://github.com/dyegolara/lnurl-auth-agents)

## Skill Output:

**Output Type(s):** [guidance, shell commands, JSON]

**Output Format:** [Markdown guidance with inline shell commands; helper output may be JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 20.19 or newer; supports LNURL_AUTH_KEYFILE for the persistent master secret path.]

## Skill Version(s):

1.4.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
