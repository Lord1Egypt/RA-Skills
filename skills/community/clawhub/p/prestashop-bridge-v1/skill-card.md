## Description:

Secure skill pack for operating a PrestaShop 9 Bridge through a stable, signed, asynchronous API contract.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ansz089](https://clawhub.ai/user/ansz089)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to guide AI agents and Python handlers that interact with a PrestaShop 9 store through a signed Bridge API. It supports synchronous product, order, and job reads, plus asynchronous product and order writes with idempotency and durable job polling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill defines write operations that can mutate product and order data in a production PrestaShop store.

Mitigation: Treat bridge:write credentials as high-impact business authority, limit them to necessary agents, enforce approval where appropriate, and poll durable job status before reporting completion.

Risk: The security verification package is incomplete because required environment and example files are missing from the artifact.

Mitigation: Require the publisher to add .env.bridge.example and examples.http, then run validators/validate_examples.py before production deployment.

Risk: Server-side image downloads are under-scoped in the security evidence.

Mitigation: Restrict image downloads to approved HTTPS asset hosts and enforce private-network, redirect, DNS rebinding, timeout, and size protections.

Risk: A 202 Accepted response can be misread as business success.

Mitigation: Always poll GET /v1/jobs/{jobId} and use MySQL-backed job status as the authority before stating that a write succeeded.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ansz089/skills/prestashop-bridge-v1)
- [Architecture Overview](docs/architecture-overview.md)
- [Environment Guide](docs/environment.md)
- [Trust and Safety](docs/trust-and-safety.md)
- [Security Model](references/security-model.md)
- [Idempotency Policy](references/idempotency-policy.md)
- [Queue Policy](references/queue-policy.md)
- [Boundary: Native PrestaShop 9 vs Bridge](references/boundary-ps9-vs-bridge.md)
- [OpenAPI Contract](openapi.yaml)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with inline HTTP, shell, JSON, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs must preserve OAuth2 client credentials, RS256 JWTs, HMAC-SHA256 request signing, idempotency headers, strict payload schemas, and asynchronous job polling.]

## Skill Version(s):

1.0.3 (source: SKILL.md frontmatter, _meta.json, README.md, openapi.yaml, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
