## Description:

Mxai helps agents use the mxai REST API to generate and transform images and videos, including MJ-style drawing, variation, upscaling, description, blend, and video workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianheihei002](https://clawhub.ai/user/tianheihei002)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to have an agent submit image, video, and MJ-style creative tasks to mxai, poll for completion, and return the resulting media links or embeds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, uploaded images, image URLs, task history queries, and account-credit checks may be sent to mxai.

Mitigation: Use the skill only when the user accepts mxai handling for the submitted content, and avoid private, regulated, or sensitive content unless that handling is approved.

Risk: MJ public mode may expose generated works beyond the private session.

Mitigation: Keep MJ public mode disabled unless the user explicitly intends to publish the generated work.

Risk: API keys and task diagnostics can appear in request or error context.

Mitigation: Mask MX_AI_API_KEY and bearer tokens in logs and avoid displaying full credential values.

Risk: Generated media links can be misleading if an agent fabricates task results or skips polling.

Mitigation: Return only URLs and status details obtained from completed mxai task-status responses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tianheihei002/skills/mxai)
- [Publisher profile](https://clawhub.ai/user/tianheihei002)
- [mxai API key portal](https://www.mxai.cn/home/#/mcp)
- [mxai REST API base](https://mcp.mxai.cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown responses with image embeds, video links, JSON-derived status details, and masked diagnostic logs when calls fail]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MX_AI_API_KEY; generated media must come from completed mxai task-status responses.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.4.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
