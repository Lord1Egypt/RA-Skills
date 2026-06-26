## Description: <br>
Query Loki logs by traceid, keywords, pod, namespace, labels, or time range to debug and analyze Kubernetes application issues via API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[peintune](https://clawhub.ai/user/peintune) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site reliability engineers use this skill to generate and run Loki API queries for Kubernetes log troubleshooting, including filtering by trace ID, keywords, pod, namespace, labels, and time range. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retrieve sensitive Loki log data from endpoints or Kubernetes port-forwards supplied by the user. <br>
Mitigation: Use least-privilege Loki or Kubernetes access, scope queries by namespace, pod, labels, time range, and result limit, and redact secrets or personal data before sharing raw log output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/peintune/loki-query) <br>
- [Publisher profile](https://clawhub.ai/user/peintune) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with shell commands and optional JSON log output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can return formatted log lines with timestamps and labels, or raw JSON when the --json flag is used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
