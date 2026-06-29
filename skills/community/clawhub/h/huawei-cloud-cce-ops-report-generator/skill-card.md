## Description: <br>
Generates consolidated Huawei Cloud CCE operations reports that combine daily inspection, capacity trends, availability risk, cost optimization, and on-call context into Markdown, HTML, and JSON outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pintudeyudi](https://clawhub.ai/user/pintudeyudi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud platform, SRE, and operations engineers use this skill to generate weekly, monthly, SLA, capacity, or stability reports for Huawei Cloud CCE clusters. It consolidates health, capacity, availability, cost, and on-call signals into reviewable operational summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence says the release is advertised as read-only reporting, but the packaged dispatcher exposes live infrastructure and monitoring mutation actions. <br>
Mitigation: Review before installing, use least-privilege read-only Huawei Cloud credentials for reports, and avoid autonomous workflows that could invoke arbitrary dispatcher actions. <br>
Risk: The skill requires sensitive Huawei Cloud credentials and can write report artifacts or raw source payloads when requested. <br>
Mitigation: Keep credentials in environment variables, avoid logging or sharing them, use a scoped output directory, and enable raw payload capture only when audit requirements justify it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pintudeyudi/huawei-cloud-cce-ops-report-generator) <br>
- [Workflow reference](references/workflow.md) <br>
- [Output schema reference](references/output-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, HTML, JSON, Files, Guidance] <br>
**Output Format:** [Markdown and HTML reports with structured JSON summaries and optional SVG charts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can persist report files to output_dir and include raw source payloads when include_raw=true.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
