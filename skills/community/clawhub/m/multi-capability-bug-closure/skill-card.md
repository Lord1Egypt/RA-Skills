## Description: <br>
Guides an agent through evidence-based bug localization and closure using source code, read-only database checks, server logs, and business platform queries before stating a root cause. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hgvgfgvh](https://clawhub.ai/user/hgvgfgvh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and support engineers use this skill to investigate bugs when they need a reproducible evidence chain across logs, database state, code paths, and platform records before deciding whether the issue is caused by data, code, configuration, or environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may access operational logs, database records, and platform data while investigating bugs. <br>
Mitigation: Use only authorized tools and limit read-only queries to the relevant issue, time window, and objects. <br>
Risk: Incomplete access to source code, database checks, server logs, or platform queries can lead to unsupported root-cause claims. <br>
Mitigation: Require the agent to report missing evidence and avoid final root-cause conclusions until the evidence chain is complete. <br>
Risk: Investigation outputs may expose sensitive data from logs or records. <br>
Mitigation: Use environment variables or secret management for credentials and avoid spreading plaintext secrets in the final report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hgvgfgvh/multi-capability-bug-closure) <br>
- [Related server log analysis skill](https://clawhub.ai/hgvgfgvh/server-log-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown investigation report with evidence, root cause, confidence, remediation steps, and verification criteria] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SQL queries, log excerpts, platform validation results, and a missing-evidence list when required capabilities are unavailable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
