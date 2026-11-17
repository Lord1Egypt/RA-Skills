## Description:

Guides agents through Amazon product-market scouting with Pangolinfo tools for demand analysis, niche filtering, benchmark product review, review-pain mining, IP checks, and go/no-go recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pangolinfo](https://clawhub.ai/user/pangolinfo)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, marketplace operators, and agent users use this skill to evaluate Amazon categories or product ideas and produce concise go/no-go product exploration reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires access to Pangolinfo-authenticated tools and the security evidence flags direct API key handling for review.

Mitigation: Configure credentials through protected MCP or secret-management paths, avoid placing API keys in prompts, URLs, tickets, or shared config, and rotate any exposed key.

Risk: Authentication or quota failures can stop the workflow and repeated retries with the same invalid key will not resolve the issue.

Mitigation: Stop on AUTH or QUOTA failures, ask the user to configure or renew credentials, and continue only after the tool connection has been restarted or reconnected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pangolinfo/skills/pangolinfo-amazon-product-explorer)
- [Pangolinfo publisher profile](https://clawhub.ai/user/pangolinfo)
- [Pangolinfo website](https://www.pangolinfo.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with tables, short recommendations, and setup commands when authentication is missing.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Pangolinfo-authenticated tools and includes clientSource="skill" in tool-call arguments.]

## Skill Version(s):

4.0.0 (source: server release metadata and changelog; artifact frontmatter states 3.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
