## Description: <br>
Unified log search across Loki, Elasticsearch, and CloudWatch with natural language queries translated to LogQL, Elasticsearch DSL, or CloudWatch filter patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tkuehnl](https://clawhub.ai/user/tkuehnl) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, SREs, and incident responders use this skill to query Loki, Elasticsearch or OpenSearch, and AWS CloudWatch logs from an agent workflow, then summarize error patterns, timelines, and likely root causes without dumping raw logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Production logs can contain PII, secrets, tokens, and internal infrastructure details that may enter the agent or LLM context. <br>
Mitigation: Install only where the agent is allowed to query observability systems, use read-only least-privilege credentials scoped to intended indices, log groups, tenants, and environments, and avoid searching logs that must not enter agent context. <br>
Risk: Broad searches can expose more sensitive log data than needed for an investigation. <br>
Mitigation: Prefer narrow time ranges, service filters, backend-specific targets, and result limits before asking the agent to analyze log output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tkuehnl/log-dive) <br>
- [Grafana Loki logcli documentation](https://grafana.com/docs/loki/latest/tools/logcli/) <br>
- [AWS CLI installation guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with inline shell commands and JSON query examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only log search results should be summarized into error groups, timelines, root-cause hypotheses, and action items; raw logs may contain sensitive data and should not be persisted or repeated unnecessarily.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
