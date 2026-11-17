## Description:

Uses CLI commands to retrieve public Douyin search results, creator posts, comments, and hot rankings as structured JSON for trend monitoring, competitor analysis, and ranking reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content analysts, and marketing teams use this skill to collect public Douyin data for short-video topic research, competitor benchmarking, comment analysis, and hot-ranking reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Douyin search terms, profile or video URLs, and GUAIKEI_API_TOKEN to the Guaikei service.

Mitigation: Install only when this data sharing is acceptable, keep GUAIKEI_API_TOKEN in an environment variable, treat it as sensitive, and rotate it if exposed.

Risk: Broad trigger rules may invoke the skill on generic trend or competitor-analysis prompts.

Mitigation: Prefer explicit Douyin-specific prompts and confirm intent before using the skill for generic market or content research.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-trending-to-ranking-report)
- [Publisher Profile](https://clawhub.ai/user/engheng-art)
- [Guaikei Service Website](https://www.guaikei.com)
- [Options Reference](references/options.md)
- [Changelog](references/changelog.md)
- [Input and Output JSON Schemas](assets/)

## Skill Output:

**Output Type(s):** [shell commands, configuration, JSON, guidance]

**Output Format:** [JSON on stdout with Markdown guidance and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >= 16.14.0 and GUAIKEI_API_TOKEN; successful runs may save JSON logs under logs/.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
