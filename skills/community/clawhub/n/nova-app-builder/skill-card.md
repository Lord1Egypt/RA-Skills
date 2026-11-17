## Description:

Build and deploy Nova Platform apps (TEE apps on Sparsity Nova / sparsity.cloud), including scaffolding, enclave application code, Docker image setup, deployment, and live-app verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zfdang](https://clawhub.ai/user/zfdang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create, configure, deploy, and verify Nova Platform TEE applications, with optional KMS, storage, attestation, and on-chain registration workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential exposure through command-line API keys or GitHub tokens embedded in remote URLs.

Mitigation: Use safer credential handling such as environment variables or a secret manager, avoid embedding tokens in Git remotes, and rotate credentials after use.

Risk: Broad network egress defaults can allow more outbound access than an application needs.

Mitigation: Review generated egress_allow settings before deployment and restrict them to the domains or IP ranges required by the app.

Risk: The skill can create files, push code, deploy cloud infrastructure, and optionally perform on-chain registration.

Mitigation: Run dry-run or preview steps first, use an empty output directory, review generated files and deployment settings, and require explicit confirmation before on-chain actions.

## Reference(s):

- [Nova Platform API Reference](references/nova-api.md)
- [Odyn Internal API Quick Reference](references/odyn-api.md)
- [Nova Platform](https://sparsity.cloud)
- [Nova Platform API Docs](https://sparsity.cloud/api/docs)
- [Nova App Template](https://github.com/sparsity-xyz/nova-app-template)
- [Nova Examples](https://github.com/sparsity-xyz/sparsity-nova-examples/)
- [Enclaver](https://github.com/sparsity-xyz/enclaver)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, generated project files, and API configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May scaffold a Dockerfile and FastAPI enclave template, provide deployment commands, and guide Nova API and optional on-chain registration steps.]

## Skill Version(s):

2.3.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
