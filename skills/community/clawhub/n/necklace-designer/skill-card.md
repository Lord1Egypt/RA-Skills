## Description:

Helps agents request jewelry design drafts and hand-drawn sketches from text and reference images, with links to interactive models when available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Jewelry designers and other users can guide an agent to draft necklace and other jewelry concepts, generate multi-view sketches, and access shared design previews using prompts, reference images, and material choices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference image URLs, and generated sessions may be sent to or hosted by the external design service.

Mitigation: Avoid sensitive inputs and review the provider's handling of generated sessions and share links before use.

Risk: Running the suggested onekey CLI through npx executes an external package.

Mitigation: Verify the CLI package source before running npx commands.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/ai-hub-admin/skills/necklace-designer)
- [Craftsman Necklace Designer](https://craftsman-agent.aiagenta2z.com/app/jewelry-designer/necklace)
- [OneKey access key setup](https://www.deepnlp.org/workspace/keys)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Markdown guidance with API examples and JSON response fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated design responses can include image URLs, design data, and shared preview links; an access key is required.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
