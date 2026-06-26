## Description: <br>
Pipeworx Pharma Analyst helps agents query integrated clinical trial, FDA drug, and RxNorm sources through an external Pipeworx MCP gateway for pharma analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Pharma analysts, researchers, and agent builders use this skill to inspect drug profiles, clinical trial pipelines, safety reports, FDA drug records, and RxNorm drug metadata from public biomedical data sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pharma research queries are sent to Pipeworx's external MCP gateway. <br>
Mitigation: Use the skill only for queries that are appropriate to share with that external service. <br>
Risk: Confidential drug strategy, proprietary sponsor questions, sensitive findings, or intentionally retained memory content may expose information beyond the local agent session. <br>
Mitigation: Avoid entering sensitive information, and use remember/recall only for information that should be retained. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-pharma-analyst) <br>
- [Pipeworx pharma analysis MCP gateway](https://gateway.pipeworx.io/mcp?task=pharma%20analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown and MCP configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces pharma data lookups and analysis summaries from external MCP tools; does not request local files, credentials, or destructive authority.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
