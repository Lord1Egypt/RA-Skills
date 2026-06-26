## Description: <br>
Validate, lint, audit, or fix PromQL queries and alerting rules while detecting anti-patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qq280948982](https://clawhub.ai/user/qq280948982) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and platform engineers use this skill to validate PromQL queries and alerting rules, detect syntax, semantic, and performance issues, and refine queries to match monitoring intent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs included local Python scripts to validate query text. <br>
Mitigation: Review the included scripts before use in restricted environments and run them only where Python 3 and local code execution are permitted. <br>
Risk: Metric type detection is heuristic-based and custom metric names may be misclassified. <br>
Mitigation: Confirm counter, gauge, histogram, or summary types with the user or metric schema before applying recommendations. <br>
Risk: The validators do not have runtime access to a Prometheus server and cannot prove that metrics or label values exist. <br>
Mitigation: Test revised queries against the target Prometheus environment before using them for production dashboards or alerts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qq280948982/promql-validator) <br>
- [PromQL best practices guide](docs/best_practices.md) <br>
- [PromQL anti-patterns guide](docs/anti_patterns.md) <br>
- [Official Prometheus querying documentation](https://prometheus.io/docs/prometheus/latest/querying/basics/) <br>
- [Prometheus metric naming practices](https://prometheus.io/docs/practices/naming/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports with inline shell commands and JSON output from local validation scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include syntax status, semantic findings, performance suggestions, query explanations, and clarifying questions.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
