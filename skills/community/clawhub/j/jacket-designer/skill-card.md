## Description:

Generates customized jacket designs for print-on-demand and manufacturing-on-demand using prompts, reference images, and structured clothing options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Designers and developers use this skill to turn jacket specifications, text or logo requests, and reference images into clothing design drafts for print or manufacturing, with links to available previews and 3D viewers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Design prompts, reference image URLs, session names, tags, and the gateway credential are sent to an external service.

Mitigation: Use the service only if this data sharing is acceptable; avoid secrets and proprietary reference URLs in prompts.

Risk: The example npx command may fetch an unpinned CLI package.

Mitigation: Prefer a pinned, trusted CLI version when using the npx example.

## Reference(s):

- [Jacket Designer on ClawHub](https://clawhub.ai/ai-hub-admin/skills/jacket-designer)
- [Craftsman Jacket Designer](https://craftsman-agent.aiagenta2z.com/app/clothing-designer/jacket)
- [OneKey access keys](https://www.deepnlp.org/workspace/keys)

## Skill Output:

**Output Type(s):** [Text, JSON request payloads, Shell commands, Design asset links]

**Output Format:** [Markdown guidance with JSON examples and links to generated designs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated results may include multi-view images, a shareable workspace, and an interactive 3D viewer when available.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
