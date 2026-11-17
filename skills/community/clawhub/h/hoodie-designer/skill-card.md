## Description:

Helps create customizable hoodie, sweatshirt, and other clothing designs from prompts, reference images, and garment specifications for print or manufacturing on demand.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Designers, merchants, and developers use this skill to prepare personalized clothing design requests and retrieve design drafts and preview links for print or manufacturing on demand. It covers multiple garment categories, not only hoodies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Design prompts, reference image URLs, logos, and related details are sent to an external design service.

Mitigation: Use only content approved for external sharing, and review the service's data practices before submitting sensitive designs.

Risk: The skill also handles clothing beyond hoodies, which may be unexpected from its name.

Mitigation: Check the selected garment category and design parameters before submitting a request.

Risk: The example CLI invocation uses an unpinned package version.

Mitigation: Prefer the documented REST request or a pinned, trusted CLI version.

## Reference(s):

- [ClawHub hoodie-designer release](https://clawhub.ai/ai-hub-admin/skills/hoodie-designer)
- [Craftsman Clothing Designer](https://craftsman-agent.aiagenta2z.com/app/clothing-designer/hoodie)
- [OneKey access keys](https://www.deepnlp.org/workspace/keys)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown with structured design requests and result links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Result links may lead to design drafts, multi-view previews, and interactive 3D workspaces when available.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
