## Description:

Guides developers in using Neon AI Gateway to call hosted language models, generate embeddings, and build agents with supported SDKs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andrelandgraf](https://clawhub.ai/user/andrelandgraf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to configure Neon AI Gateway and integrate hosted model calls, embeddings, or agents into applications through familiar SDKs. It provides setup guidance and implementation examples for branch-scoped inference.

### Deployment Geography for Use:

AWS us-east-1, us-east-2, eu-central-1, and ap-southeast-1

## Known Risks and Mitigations:

Risk: The example todo tool returns database rows without showing user or tenant scoping, which could expose other users’ records to a model.

Mitigation: Enforce authenticated user or tenant isolation, filter records appropriately, and return only necessary fields before sending data to hosted inference.

Risk: Local gateway token files could expose credentials if mishandled.

Mitigation: Protect local token files and avoid sharing or committing gateway credentials.

Risk: Gateway configuration changes may affect a branch when applied.

Mitigation: Preview the configuration plan before applying changes or deploying.

## Reference(s):

- [Neon AI Gateway overview](https://neon.com/docs/ai-gateway/overview.md)
- [Neon AI Gateway authentication](https://neon.com/docs/ai-gateway/authentication.md)
- [Neon AI Gateway models](https://neon.com/docs/ai-gateway/models.md)
- [Neon AI Gateway embeddings guide](https://neon.com/docs/ai-gateway/embeddings)
- [Neon AI Gateway troubleshooting](https://neon.com/docs/ai-gateway/troubleshooting.md)
- [Neon model catalog on models.dev](https://models.dev/providers/neon)
- [Vercel AI SDK](https://ai-sdk.dev)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Technical guidance]

**Output Format:** [Markdown with TypeScript and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include SDK integration examples, gateway setup steps, and troubleshooting guidance.]

## Skill Version(s):

1.0.6 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
