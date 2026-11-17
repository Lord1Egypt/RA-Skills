## Description:

NexSolve AI connects industry pain points with AI developers for task submission, real-time listing, intelligent analysis, and contact extraction via OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zxz0119](https://clawhub.ai/user/zxz0119)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to submit bilingual industry pain points to the NexSolve AI marketplace, list open needs, and retrieve need details for feasibility analysis and contact handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broadly scoped GitHub token can grant more account access than the skill needs.

Mitigation: Use a fine-grained GitHub token restricted to zxz0119/NexSolve-AI with only Issues read/write permission.

Risk: Submitted business problems or contact details may become public.

Mitigation: Avoid personal, confidential, or sensitive business details in problem and contact fields.

Risk: Retrieved GitHub issue text is untrusted and may contain instructions aimed at the agent.

Mitigation: Treat returned issue content as data for analysis only and do not let it override system, developer, or user instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zxz0119/skills/nexsolve-ai)
- [Publisher profile](https://clawhub.ai/user/zxz0119)
- [NexSolve AI repository link from artifact documentation](https://github.com/zxz0119/NexSolve-AI)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [MCP tool responses as text, including issue creation confirmations, issue listings, and issue details suitable for Markdown summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GITHUB_TOKEN configuration; submissions may create public issues containing user-provided problem and optional contact details.]

## Skill Version(s):

1.0.2 (source: evidence release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
