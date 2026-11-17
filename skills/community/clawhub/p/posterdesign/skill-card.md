## Description:

claw_poster helps agents create posters and social images by searching visual-rag templates, filling text slots, rendering PNGs, and checking output quality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zooagentpm](https://clawhub.ai/user/zooagentpm)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and agents use this skill to turn poster, cover, and event-image requests into rendered PNG designs. It guides template selection, slot filling, rendering, and quality checks for models with or without visual inspection capabilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User design content is sent to a temporary external MCP service whose operator cannot be clearly verified.

Mitigation: Install only if you trust the publisher and endpoint operator, and avoid sending confidential campaign plans, customer data, credentials, or sensitive brand material.

Risk: Generated images and download links may be unsuitable for public use without review.

Mitigation: Review generated images, quality reports, and download links before publishing or sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zooagentpm/skills/posterdesign)
- [visual-rag MCP endpoint](https://syncopated-retractively-anitra.ngrok-free.dev/mcp)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Files]

**Output Format:** [Chat text with MCP tool calls, PNG image outputs, download links, and quality-check reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill expects agents to inspect generated render and annotation images before returning final assets.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
