## Description:

Run a full McKinsey-level market research and strategy analysis using 12 specialized prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abdullah4ai](https://clawhub.ai/user/abdullah4ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and business teams use this skill to run structured market research, competitive analysis, pricing, go-to-market, financial modeling, risk, and executive strategy synthesis workflows for a business idea or operating company.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use web research, launch multiple sub-agents, and save business analysis files locally.

Mitigation: Install from a trusted, pinned channel when possible, avoid providing credentials or confidential financial details, and review generated artifacts before sharing.

Risk: Market sizing, competitor data, and financial projections can become outdated or assumption-heavy.

Mitigation: Require verifiable citations, source dates, and explicit assumptions; have a qualified reviewer check business-critical recommendations.

Risk: Local report and data files persist in the workspace and may be readable by other skills in the same environment.

Mitigation: Keep sensitive inputs out of artifact files and remove or restrict generated reports when they are no longer needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/abdullah4ai/skills/mckinsey-research)
- [Security Guidance](references/security.md)
- [Variable Map](references/variable-map.md)
- [Strategy Prompts](references/prompts.md)
- [Prompt Library](references/prompts/)
- [Gotchas](references/gotchas.md)
- [Saudi Market Reference](references/saudi-market.md)
- [Industry Benchmarks Reference](references/benchmarks.md)
- [Report Template](templates/report.html)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown summaries and self-contained HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves individual analyses and a final report under artifacts/research/; reports should cite verifiable market sources and state assumptions.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
