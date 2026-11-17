## Description:

Analyzes the top 10 leading enterprises in a given industry by market value or revenue and produces a sourced Markdown ranking table with per-company deep dives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zrxparley](https://clawhub.ai/user/zrxparley)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and agent operators use this skill to research leading companies in an industry and generate a sourced Top 10 report. It can run standalone or as the first stage of an industry-analysis workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Industry names, scope, time window, and search terms may be sent to external web services during research.

Mitigation: Avoid confidential inputs and review the intended search scope before running the skill.

Risk: Company rankings, market values, revenue, and market-share details may be stale, incomplete, or uncertain.

Mitigation: Require the report to state the ranking basis, data time window, and sources, and to explicitly mark unresolved or uncertain findings.

Risk: The skill writes a Markdown report and may update a session status file under the selected output directory.

Mitigation: Confirm the output directory before execution and review changed files after the skill completes.

## Reference(s):

- [Top 10 output template](references/top-10-template.md)
- [ClawHub skill release](https://clawhub.ai/zrxparley/skills/industry-analyzer-top-enterprise)

## Skill Output:

**Output Type(s):** [markdown, text, configuration]

**Output Format:** [Markdown report with a ranking table and per-company sections, plus a session JSON status update when session state is used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes output/{industry-slug}/01-top-enterprise.md and updates output/{industry-slug}/session.json; uncertain findings are expected to be explicitly marked.]

## Skill Version(s):

0.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
