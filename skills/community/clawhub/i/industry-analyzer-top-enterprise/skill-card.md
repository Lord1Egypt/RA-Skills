## Description: <br>
Analyzes the top 10 leading enterprises in an industry by market value or revenue and produces a sourced Markdown ranking table with per-company deep dives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zrxparley](https://clawhub.ai/user/zrxparley) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and developers use this skill to research the leading companies in a specified industry, compare them by market value or revenue, and generate a cited Top 10 company report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated report may contain incorrect or outdated market, revenue, valuation, or company ranking data. <br>
Mitigation: Review the cited public sources and the stated sorting basis before relying on the report for business decisions. <br>
Risk: The skill writes or updates files under an industry output directory. <br>
Mitigation: Run it in an expected workspace and review changes to the generated Markdown report and session.json before using them downstream. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zrxparley/industry-analyzer-top-enterprise) <br>
- [Top 10 output template](artifact/references/top-10-template.md) <br>
- [Publisher profile](https://clawhub.ai/user/zrxparley) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Research guidance, Configuration] <br>
**Output Format:** [Markdown report plus session.json status and source updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes output/{industry-slug}/01-top-enterprise.md and updates output/{industry-slug}/session.json when a session is used.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
