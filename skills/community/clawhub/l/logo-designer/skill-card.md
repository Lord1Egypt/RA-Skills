## Description:

Generates multi-page logo design image carousels from logo-designer templates using the Craftsman image generator through the OneKey Agent Gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to call a hosted image-generation API that creates editable logo-design carousel sessions from prompts, reference images, layout settings, styles, and asset-size parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional CLI path runs an unpinned npm package while exposing an API key.

Mitigation: Prefer the direct HTTPS API example, or pin and verify the one key CLI package version before use.

Risk: Prompts and images are sent to a third-party DeepNLP/Craftsman service.

Mitigation: Do not send confidential images, regulated data, or private prompts unless the service's data handling is acceptable for the intended use.

Risk: A leaked or reused OneKey access key could authorize unwanted API usage.

Mitigation: Use a restricted key where possible and rotate it after testing untrusted tooling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ai-hub-admin/skills/logo-designer)
- [Craftsman image generator console](https://craftsman-agent.aiagenta2z.com/app/image-generator)
- [Craftsman website](https://craftsman-agent.aiagenta2z.com)
- [DeepNLP workspace keys](https://deepnlp.org/workspace/keys)
- [OneKey router API endpoint](https://agent.deepnlp.org/agent_router)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON]

**Output Format:** [Markdown with bash and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces hosted image URLs, share URLs, session metadata, and editable page/layer configuration from the remote API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
