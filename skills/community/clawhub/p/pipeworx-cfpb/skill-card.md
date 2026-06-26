## Description: <br>
Search and retrieve CFPB consumer complaint data through a Pipeworx MCP server, including complaint details, company summaries, top complaint companies, and product breakdowns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[b-gutman](https://clawhub.ai/user/b-gutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query CFPB consumer complaint records, inspect company complaint activity, and summarize complaint patterns by company, product, keyword, or date range. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Complaint narratives and complaint details may include sensitive consumer financial information. <br>
Mitigation: Use the retrieved data only in appropriate workflows and apply organizational privacy, retention, and sharing controls. <br>
Risk: Security guidance notes that moderation or maintenance workflows can affect real users and skills when those workflows are present. <br>
Mitigation: Review any moderation or maintenance actions before execution and run the skill only with the permissions needed for the intended task. <br>
Risk: Security guidance notes that autoreview helpers may run with broad local access or share diffs with configured local AI review tools unless opted out. <br>
Mitigation: Confirm local access and review-tool settings before enabling any autoreview workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/b-gutman/pipeworx-cfpb) <br>
- [Publisher profile](https://clawhub.ai/user/b-gutman) <br>
- [Pipeworx CFPB MCP endpoint](https://gateway.pipeworx.io/cfpb/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON MCP server configuration and text responses from MCP tools] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connects agents to the hosted CFPB MCP endpoint without an API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
