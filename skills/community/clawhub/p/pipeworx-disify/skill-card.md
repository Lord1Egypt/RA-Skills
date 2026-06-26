## Description: <br>
Detect disposable and temporary email addresses — validate emails and check domains against known throwaway services <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to validate sign-up, lead-generation, user-database, and anti-abuse workflows for disposable or malformed email usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Email addresses or domains checked with the skill are sent to Pipeworx's remote Disify service. <br>
Mitigation: Avoid sensitive, regulated, or bulk customer data unless your organization has reviewed Pipeworx's privacy, logging, and retention practices. <br>


## Reference(s): <br>
- [Pipeworx Disify homepage](https://pipeworx.io/packs/disify) <br>
- [Pipeworx Disify MCP endpoint](https://gateway.pipeworx.io/disify/mcp) <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-disify) <br>
- [Publisher profile](https://clawhub.ai/user/brucegutman) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON examples and MCP configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for the documented direct API example and uses a remote Pipeworx MCP service.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
