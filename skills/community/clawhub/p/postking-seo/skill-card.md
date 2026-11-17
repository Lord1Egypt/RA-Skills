## Description:

Run SEO / GEO from seed keywords to published, AI-citation-friendly articles using PostKing: seed, expand, cluster, roadmap, brief, write, and publish.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bitsandtea](https://clawhub.ai/user/bitsandtea)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, founders, and content operators use this skill to turn seed keywords into clustered SEO/GEO content roadmaps, briefs, draft articles, and published or scheduled posts for an onboarded PostKing brand.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish or schedule content to a live website.

Mitigation: Require the agent to show the exact article, target publication, schedule, and review or rollback path before any publish or schedule operation.

Risk: Batch CTA assignment can affect many posts, especially with broad targets such as blogIds:"all".

Mitigation: Use explicit blog ID lists whenever possible and confirm overwrite or Webflow inclusion settings before execution.

Risk: Cluster delete and merge operations can permanently change roadmap, brief, and article organization.

Mitigation: Review the affected cluster IDs and expected cascade before delete or merge operations, and prefer reversible rejection workflows when deletion is not required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bitsandtea/skills/postking-seo)
- [PostKing MCP endpoint](https://mcp.postking.app/mcp)
- [PostKing SEO icon](https://raw.githubusercontent.com/bitsandtea/postking-skills/main/assets/icons/postking-seo.svg)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with tool-call and CLI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose live PostKing publishing, scheduling, CTA assignment, delete, and merge operations that require user review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
