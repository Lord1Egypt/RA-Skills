## Description: <br>
Analyze federal government contracting data from SAM.gov, USAspending, and SBIR to profile contractors, find opportunities, and assess agency spending. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Government contracting, capture, and business development analysts use this skill to research contractors, scan federal opportunities, and assess agency spending patterns from public GovCon data sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GovCon searches, contractor names, opportunity interests, and related analysis prompts are sent to the remote Pipeworx MCP gateway. <br>
Mitigation: Do not submit confidential procurement strategy, sensitive business findings, or other information that should not be processed by the gateway. <br>
Risk: The skill exposes remember and recall behavior for saving intermediate findings. <br>
Mitigation: Store only information intended to persist, and avoid saving confidential or sensitive procurement analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-govcon-analyst) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with MCP server configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing GovCon analysis, search guidance, and setup configuration for a remote Pipeworx MCP gateway.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
