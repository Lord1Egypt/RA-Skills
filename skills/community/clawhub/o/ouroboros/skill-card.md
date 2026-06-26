## Description: <br>
Ouroboros routes messages starting with `ooo` to the `ouroboros_channel_workflow` MCP tool and relays the tool response without adding independent answers, code, or summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[q00](https://clawhub.ai/user/q00) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams using OpenClaw use this skill to route `ooo` requests into an external Ouroboros MCP workflow for interviewing, seed generation, execution, status checks, and repository context. The agent acts as a relay and does not reinterpret the request or generate its own answer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill delegates repository and execution-related work to an external Ouroboros MCP server and unpinned `ouroboros-ai` package. <br>
Mitigation: Review or pin the MCP package before installation and use it only in channels and repositories where the server's access and retention behavior is acceptable. <br>
Risk: The skill passes channel, guild, user, message, and repository context to the MCP workflow. <br>
Mitigation: Confirm the data sent through `repo`, `run`, and stored message identifiers before using the skill in private channels or important repositories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/q00/ouroboros) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Tool call arguments plus relayed plain text or Markdown responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an external Ouroboros MCP server configured through OpenClaw; responses are relayed without reinterpretation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
