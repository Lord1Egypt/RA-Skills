## Description: <br>
Provides access to US FDA open data for adverse drug event reports, drug labeling/package inserts, and food recall enforcement actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[b-gutman](https://clawhub.ai/user/b-gutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and healthcare or product-safety teams use this skill to query public FDA datasets for adverse event investigations, prescribing information checks, food recall monitoring, and pharmacovigilance research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: FDA lookup queries are sent to Pipeworx's hosted gateway. <br>
Mitigation: Do not include patient identifiers, private case details, or internal pharmacovigilance notes unless the gateway and its query-log handling have been approved for that data. <br>
Risk: The documented MCP configuration uses mcp-remote@latest, which can change between installs. <br>
Mitigation: Pin mcp-remote to a reviewed version for repeatable deployments. <br>


## Reference(s): <br>
- [Pipeworx FDA pack](https://pipeworx.io/packs/fda) <br>
- [ClawHub listing](https://clawhub.ai/b-gutman/pipeworx-fda) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON MCP configuration and shell command examples; tool calls return FDA public-data results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for the documented direct request example; MCP configuration uses mcp-remote to connect to the Pipeworx hosted FDA gateway.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
