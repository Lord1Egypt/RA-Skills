## Description: <br>
Build ORBCAFE chat and copilot experiences with AgentPanel, StdChat, CopilotChat, ChatMessage typing flow, and AgentUICardHooks using official examples patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SHENRUIYANG](https://clawhub.ai/user/SHENRUIYANG) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build ORBCAFE full-page chat and floating copilot interfaces with public orbcafe-ui APIs. It helps select AgentPanel, StdChat, or CopilotChat and produce minimal code, state shape, verification steps, and troubleshooting guidance for streaming replies and card actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Frontend setup commands install ORBCAFE UI and peer packages into the target React project. <br>
Mitigation: Install only in the intended project and review package versions through the normal lockfile and version-pinning workflow before running setup commands. <br>
Risk: Chat, streaming, card action, drag, or resize behavior can appear visible but have no effect if required state and hook contracts are not wired. <br>
Mitigation: Follow the public API, message state, streaming completion, card hook, and copilot shell guardrails before accepting the implementation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/SHENRUIYANG/orbcafe-agentui-chat) <br>
- [Component Selection](references/component-selection.md) <br>
- [AgentUI Guardrails](references/guardrails.md) <br>
- [AgentUI Recipes](references/recipes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with TypeScript/TSX and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes component selection, minimal code, state shape, verification steps, and troubleshooting.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
