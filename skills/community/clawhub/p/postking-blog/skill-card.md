## Description:

Create blog publications and generate, iterate on, and publish articles on PostKing, hosted or pushed to WordPress, Medium, or Substack.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bitsandtea](https://clawhub.ai/user/bitsandtea)

### License/Terms of Use:

MIT-0

## Use Case:

External users and marketing teams use this skill to manage PostKing blog publications, generate and revise articles, and publish or schedule content to hosted blogs or connected WordPress, Medium, and Substack channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Blog updates, publication changes, deletes, schedules, or external publishing can affect public or persistent content.

Mitigation: Confirm the target brand, publication, article, and external connection IDs before publish, schedule, update, import, or delete actions.

Risk: Generated or revised article content may be published before the user has reviewed the final copy and metadata.

Mitigation: Review the article body, SEO fields, featured image, CTA, preview URL, and publish destination before making content live.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bitsandtea/skills/postking-blog)
- [PostKing MCP endpoint](https://mcp.postking.app/mcp)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Markdown, Text]

**Output Format:** [Markdown guidance with MCP tool-call parameters, optional shell commands, and generated or edited blog text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, update, publish, schedule, import, or delete persistent blog content when the user directs those actions.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
