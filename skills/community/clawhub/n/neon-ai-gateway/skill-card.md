## Description:

Guides developers in routing LLM and embedding requests through Neon's branch-scoped AI Gateway using familiar SDKs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andrelandgraf](https://clawhub.ai/user/andrelandgraf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to configure Neon AI Gateway for applications and agents that call language or embedding models. It provides SDK examples, setup guidance, and advice for checking model availability and branch credentials.

### Deployment Geography for Use:

AWS regions aws-us-east-2, aws-us-east-1, aws-eu-central-1, and aws-ap-southeast-1.

## Known Risks and Mitigations:

Risk: An example may send database records to hosted inference, exposing more data than intended.

Mitigation: Review the query and destination, limit fields to what the model needs, and confirm access is scoped to the intended user.

Risk: The security scan was partial, so its results may miss issues.

Mitigation: Inspect the skill and example flows before installation, and review the Neon CLI workflow you trust.

## Reference(s):

- [Neon AI Gateway overview](https://neon.com/docs/ai-gateway/overview.md)
- [Neon AI Gateway getting started](https://neon.com/docs/ai-gateway/get-started.md)
- [Neon AI Gateway troubleshooting](https://neon.com/docs/ai-gateway/troubleshooting.md)
- [Neon model catalog](https://models.dev/providers/neon)
- [Neon AI Gateway prepaid credits](https://neon.com/docs/ai-gateway/prepaid-credits.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions, API calls]

**Output Format:** [Markdown guidance with TypeScript, shell, and API examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples use branch-scoped credentials; model availability depends on the live catalog and account access.]

## Skill Version(s):

1.0.8 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
