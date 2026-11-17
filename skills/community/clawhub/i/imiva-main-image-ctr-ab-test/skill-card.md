## Description:

This skill helps brand merchants, ecommerce operators, designers, and content teams use IMIVA MCP to generate main-image A/B test variants while preserving confirmed product facts and supporting budget confirmation, task tracking, and result delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce teams and content creators use this skill to turn confirmed product materials, selling points, channel requirements, and budget constraints into IMIVA MCP image-generation tasks for CTR-oriented main image variants.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned npm MCP package with token and broad environment access.

Mitigation: Use a dedicated low-privilege IMIVA token, avoid shells with unrelated secrets, set the API endpoint to the official IMIVA service, and prefer a pinned reviewed npm package version.

Risk: Image-generation tasks can consume credits when submitted.

Mitigation: Confirm budget, generation count, model, specifications, and task details before creating a task, and keep task IDs for follow-up instead of creating duplicates.

Risk: Generated ecommerce visuals may contain inaccurate product facts, claims, pricing, or unauthorized reference content.

Mitigation: Use only user-confirmed product facts and authorized materials, then review outputs for product accuracy, claims, copyright, likeness, and platform rules before publication.

## Reference(s):

- [IMIVA homepage](https://imiva.ecpro.com/)
- [MCP configuration example](references/mcp-config.example.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call IMIVA MCP tools after token, budget, and task details are confirmed.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
