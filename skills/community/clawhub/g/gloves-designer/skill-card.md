## Description:

Helps agents create customized glove design drafts for print-on-demand and manufacturing-on-demand from prompts, structured options, and reference images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Designers, developers, and print-on-demand teams use this skill to specify glove materials, sizing, decoration, and reference images, then request design drafts through an external clothing-design service. The same service supports other clothing categories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Design prompts and reference image URLs are submitted to an external service.

Mitigation: Do not submit confidential designs, private image URLs, secrets, or regulated data without reviewing the service and its retention policy.

Risk: The OneKey access key grants access to the external gateway.

Mitigation: Store the key as a secret and avoid including it in prompts or shared outputs.

Risk: The skill includes an unpinned npx onekey example.

Mitigation: Vet or pin the package before running the example.

## Reference(s):

- [Gloves Designer on ClawHub](https://clawhub.ai/ai-hub-admin/skills/gloves-designer)
- [Craftsman Gloves Designer](https://craftsman-agent.aiagenta2z.com/app/clothing-designer/gloves)
- [OneKey access keys](https://www.deepnlp.org/workspace/keys)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands]

**Output Format:** [Markdown with JSON request examples and links to externally generated designs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The external service may return a shared workspace URL, multi-view image links, and design blueprint data; 3D assets depend on availability.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
