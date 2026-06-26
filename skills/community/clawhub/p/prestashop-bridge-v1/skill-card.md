## Description: <br>
Secure skill pack for operating a PrestaShop 9 Bridge through a stable, signed, asynchronous API contract. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ansz089](https://clawhub.ai/user/Ansz089) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to guide AI agents and Python handlers that interact with a PrestaShop 9 store through a signed Bridge API. It supports synchronous reads, asynchronous product and order writes, idempotent job handling, and durable job polling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide changes to live store data, including product imports, price or stock changes, SEO edits, and order-status updates. <br>
Mitigation: Require explicit confirmation before write operations and poll job status before reporting business completion. <br>
Risk: The security review reports an unlabeled signing secret in the validator and warns not to reuse the embedded HMAC value. <br>
Mitigation: Use deployment-specific HMAC secrets, rotate or reject any copied sample secret, and keep secrets out of source control. <br>
Risk: Publisher and import provenance require review before production use because server-resolved GitHub import provenance is unavailable. <br>
Mitigation: Verify the publisher profile and package contents before deployment, and install only when the Bridge operator controls the target PrestaShop environment. <br>
Risk: Asynchronous writes use at-least-once delivery, so duplicate processing is possible without correct idempotency handling. <br>
Mitigation: Preserve `X-Request-ID` for retries, enforce business idempotency in MySQL, and follow the documented job polling policy. <br>


## Reference(s): <br>
- [PrestaShop Bridge V1 ClawHub Page](https://clawhub.ai/Ansz089/prestashop-bridge-v1) <br>
- [OpenAPI Contract](openapi.yaml) <br>
- [Quickstart](docs/quickstart.md) <br>
- [Environment Guide](docs/environment.md) <br>
- [Trust and Safety](docs/trust-and-safety.md) <br>
- [Security Model](references/security-model.md) <br>
- [Idempotency Policy](references/idempotency-policy.md) <br>
- [Queue Policy](references/queue-policy.md) <br>
- [Boundary: Native PrestaShop 9 vs Bridge](references/boundary-ps9-vs-bridge.md) <br>
- [Release Notes 1.0.3](docs/release-notes-1.0.3.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTTP/API contract details, JSON examples, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance should preserve OAuth2, HMAC, idempotency, asynchronous write, and job polling requirements.] <br>

## Skill Version(s): <br>
1.0.3 (source: SKILL.md frontmatter, _meta.json, README.md, openapi.yaml, release notes, and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
