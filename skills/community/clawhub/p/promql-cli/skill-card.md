## Description: <br>
CLI for querying Prometheus and PromQL-compatible engines, including instant queries, range queries, metric discovery, table/csv/json/graph output, and PromQL troubleshooting guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site reliability engineers use this skill to run promql-cli queries, discover Prometheus metrics and labels, visualize time series, and investigate latency, error, saturation, and other observability issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide use of Prometheus credentials or bearer tokens while configuring promql-cli. <br>
Mitigation: Keep credentials in local files with restricted permissions and avoid passing tokens or passwords through chat, command arguments, shell history, or process listings. <br>
Risk: The skill runs promql-cli commands against user-selected Prometheus-compatible endpoints and can expose operational metrics in outputs. <br>
Mitigation: Confirm the intended Prometheus host and scope before running queries, and avoid sharing sensitive metric labels or results outside the authorized environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/samber/promql-cli) <br>
- [Publisher profile](https://clawhub.ai/user/samber) <br>
- [Source skill collection](https://github.com/samber/cc-skills) <br>
- [promql-cli documentation](https://github.com/nalbury/promql-cli) <br>
- [promql-cli releases](https://github.com/nalbury/promql-cli/releases) <br>
- [Installation reference](references/installation.md) <br>
- [Usage reference](references/usage.md) <br>
- [Graphing reference](references/graphing.md) <br>
- [Debugging methodology](references/debugging.md) <br>
- [PromQL reference](references/promql-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline PromQL and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include promql-cli command lines, PromQL expressions, jq pipelines, setup guidance, and analysis of table, CSV, JSON, or ASCII graph output.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
