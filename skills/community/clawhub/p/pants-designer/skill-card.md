## Description:

Helps agents generate customized pants and other clothing design drafts for print-on-demand and manufacturing-on-demand using prompts, structured options, and reference images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Designers and print-on-demand or manufacturing teams use this skill to request clothing design drafts, including pants and trousers, and share generated design previews through the Craftsman service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Design prompts, reference image URLs, and metadata are sent to an external clothing-design service using an API key.

Mitigation: Use the service only when approved; avoid confidential designs and private image URLs unless you trust the provider, and protect the API key.

Risk: An example invokes CLI tooling through npx.

Mitigation: Prefer a pinned or reviewed CLI package before running the example.

Risk: The skill covers clothing beyond the pants-focused name.

Mitigation: Review the requested clothing template and design parameters before sending a request.

## Reference(s):

- [ClawHub pants-designer release](https://clawhub.ai/ai-hub-admin/skills/pants-designer)
- [Craftsman pants designer](https://craftsman-agent.aiagenta2z.com/app/clothing-designer/pants)
- [OneKey agent gateway](https://agent.deepnlp.org/agent_router)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Shell commands]

**Output Format:** [Markdown with JSON request examples and design-result links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The external service may return design previews, multi-view images, blueprints, and a shareable workspace URL.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
