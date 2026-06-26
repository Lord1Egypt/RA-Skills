## Description: <br>
Structured 8-step framework for designing production AI agents, including task selection, step mapping, I/O specification, system prompts, memory, safeguards, interface choice, and testing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wholeinsoul](https://clawhub.ai/user/wholeinsoul) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and teams use this skill to design a new AI agent, plan an automated workflow, or review an existing agent design before implementation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents designed with this framework may later receive tools, credentials, memory stores, or action permissions that are outside the skill artifact itself. <br>
Mitigation: Review each added integration separately, restrict credentials and permissions to the minimum needed, and log tool calls and decisions for audit. <br>
Risk: High-impact actions such as email, data changes, spending, deletion, or publishing can cause harm if automated without review. <br>
Mitigation: Require human approval for those actions and test the agent with real examples before deployment. <br>


## Reference(s): <br>
- [AI Agent Building Guide - Complete Reference](references/guide.md) <br>
- [Production Agent Builder on ClawHub](https://clawhub.ai/wholeinsoul/production-agent-builder) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown design document] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces an agent design covering task and success criteria, step map, I/O specification, system prompt, memory architecture, safeguards, interface, and test plan.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
