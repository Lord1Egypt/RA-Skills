## Description:

Max Auth is a security authentication gate for OpenClaw sensitive actions that deploys a local Node.js auth server with biometric passkeys, master password login, session-scoped auth, one-time secret submission URLs, and a browser UI in Portuguese, English, and Spanish.

This skill is ready for commercial/non-commercial use.

## Publisher:

[felipematos](https://clawhub.ai/user/felipematos)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Max Auth to require local authentication before sensitive OpenClaw actions and to collect secrets through one-time HTTPS forms instead of chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shipped server does not enforce several advertised protections for sensitive-action authentication.

Mitigation: Do not use the skill to protect real sensitive actions or collect real credentials until the security guidance items are fixed and retested.

Risk: SessionKey isolation, returnUrl token handling, secret API authorization, CORS, XSS-safe rendering, and dependency locking require remediation according to the release security guidance.

Mitigation: Restrict use to non-sensitive evaluation until those controls are reviewed, fixed, and retested.

## Reference(s):

- [Max Auth ClawHub Skill Page](https://clawhub.ai/felipematos/skills/max-auth)
- [Max Auth - Setup & API Reference](references/api.md)
- [OpenClaw Agent Integration Guide](references/integration.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, API calls]

**Output Format:** [Markdown with inline shell, JSON, and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return local auth URLs, one-time secret submission URLs, auth status checks, and deployment configuration guidance.]

## Skill Version(s):

2.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
