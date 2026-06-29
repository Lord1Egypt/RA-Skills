## Description: <br>
Kechuang Collection monitors public science-and-technology policy sources and filters leads that match company innovation KPI criteria. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cryptocxf](https://clawhub.ai/user/cryptocxf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business, strategy, and innovation teams use this skill to scan public Chinese government, industry, and official science-and-technology sources for grant, award, certification, standards, and project leads. The skill helps prioritize leads against a configurable KPI rubric and produce summaries for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill searches public web sources and saves lead reports or logs locally. <br>
Mitigation: Install only in environments where public-web collection is acceptable, and periodically review or delete local leads-output files on shared machines. <br>
Risk: Background monitoring and notification behavior is under-specified in the security evidence. <br>
Mitigation: Treat monitor and notification claims as environment-dependent unless the target agent runtime explicitly supports those tools. <br>
Risk: Collected leads are planning aids and may be incomplete, stale, or mismatched to a company's actual eligibility. <br>
Mitigation: Manually verify high-value leads, deadlines, source terms, and application requirements before acting on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cryptocxf/kechuang-collection) <br>
- [KPI criteria and lead matching rules](references/kpi-criteria.md) <br>
- [Monitoring sources](references/monitoring-sources.md) <br>
- [Quick start guide](references/quick-start.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Guidance] <br>
**Output Format:** [Markdown reports, tabular lead summaries, JSON lead files, and local log files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save scan outputs, reports, and monitoring logs under a local leads-output directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata, changelog, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
