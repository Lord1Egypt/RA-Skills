## Description: <br>
Generates structured industry analysis reports by gathering sourced market, competitive, policy, trend, and investment data, then producing a polished Markdown report with HTML or PDF output when possible. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangmanqi2104201431-ship-it](https://clawhub.ai/user/yangmanqi2104201431-ship-it) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and strategy teams use this skill to generate sourced industry research reports covering market size, competitors, policy, trends, risks, and investment opportunities. It is suited for market research and decision-support workflows where citations, data-cutoff dates, and uncertainty labels are important. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Industry topics, company plans, deal themes, or market-entry ideas may be exposed through web searches. <br>
Mitigation: Avoid confidential or sensitive topics unless the user is comfortable with those terms being sent to search providers. <br>
Risk: Generated HTML or PDF reports may be written into a shared working directory. <br>
Mitigation: Check or choose the output directory before running the skill in shared environments. <br>
Risk: Reports can contain inferred, forecast, stale, or conflicting market data when source coverage is limited. <br>
Mitigation: Review citations, data-cutoff dates, forecast labels, and inferred-data labels before using the report for decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yangmanqi2104201431-ship-it/industry-analysis) <br>
- [Report template](references/report-template.md) <br>
- [Source guidelines](references/source-guidelines.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown industry report rendered to styled HTML, with PDF output when conversion tools are available.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses web search, records source URLs and publication dates, labels inferred or forecast data, and saves report files in the current working directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
