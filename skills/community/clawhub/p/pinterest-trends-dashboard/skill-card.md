## Description:

Helps users plan a Pinterest affiliate trends dashboard that ranks ClickBank niches, estimates search demand, and surfaces payout-driven opportunity scores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marlowne12](https://clawhub.ai/user/marlowne12)

### License/Terms of Use:

MIT-0

## Use Case:

Affiliate marketers and builders use this skill to turn ClickBank niche, Pinterest trend, and payout assumptions into a dashboard specification, mockup, and implementation plan. It supports niche comparison, sub-niche drilldown, opportunity scoring, and export-oriented dashboard design.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The browser mockup loads frontend dependencies from mutable CDNs.

Mitigation: Pin and bundle frontend dependencies before production deployment.

Risk: Deployment examples include optional cron jobs, auto-deploy, analytics, and affiliate-link workflows.

Mitigation: Enable automation and outbound affiliate-link behavior only after reviewing destinations, credentials, schedules, and analytics settings.

Risk: Niche revenue, search volume, and payout values are estimates or cached planning data.

Mitigation: Validate and date data sources before using the dashboard for business decisions.

## Reference(s):

- [Brief, PRD, and Architecture](BRIEF_PRD_ARCH.md)
- [Design Rationale](DESIGN_MOCKUPS/DESIGN_RATIONALE.md)
- [Interactive Design Mockup](DESIGN_MOCKUPS/preview.html)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown specification with JSON, JavaScript, shell command examples, and an HTML dashboard mockup]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces planning and design artifacts for an agent-assisted dashboard build; production use requires dependency pinning and intentional workflow configuration.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
