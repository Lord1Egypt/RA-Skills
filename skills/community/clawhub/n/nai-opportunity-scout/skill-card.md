## Description: <br>
Opportunity Scout helps agents find and prioritize user pain points and unmet demand across Reddit, Hacker News, and configurable sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, founders, product researchers, and developers use this skill to scan public forums for demand signals, score candidate opportunities, and generate prioritized market-research digests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated opportunity reports may be incomplete, stale, or misleading when public-source signals are sparse, noisy, or unrepresentative. <br>
Mitigation: Treat reports as research leads and verify demand, competition, and market context before making product or business decisions. <br>
Risk: The bundled workflow can perform web searches and write configuration, findings, history, and digest files locally, including on a recurring schedule if cron is enabled. <br>
Mitigation: Review configured sources, schedule, and output paths before running scans; enable cron only when recurring local reports are intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/newageinvestments25-byte/nai-opportunity-scout) <br>
- [Demand Signal Types](references/signal-types.md) <br>
- [Source Configuration Guide](references/source-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON query and scoring data, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores configuration, findings, and signal history locally when the bundled scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
