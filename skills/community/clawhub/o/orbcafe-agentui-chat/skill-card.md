## Description:

Build ORBCAFE chat and copilot experiences with AgentPanel, StdChat, CopilotChat, ChatMessage typing flow, and AgentUICardHooks using official example patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenruiyang](https://clawhub.ai/user/shenruiyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to build ORBCAFE full-page chat and floating copilot interfaces using AgentPanel, StdChat, CopilotChat, streaming message state, card hooks, and public ORBCAFE APIs. It also helps troubleshoot visible chat UIs where send, streaming, card actions, drag, or resize behavior has no effect.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency changes may install ORBCAFE and MUI packages into the user's project.

Mitigation: Review package changes before running the listed npm install command or starting the example dev server.

Risk: Chinese-language implementation guidance may be hard to review for teams that cannot validate the instructions directly.

Mitigation: Use a reviewer who can read the guidance to confirm component choice, state handling, verification steps, and troubleshooting output.

Risk: Copilot drag or resize behavior can appear broken if shell state and resize observer behavior are wired incorrectly.

Mitigation: Keep floating button, open state, positioning, drag, snap, and resize logic in the page shell, and suspend resize observer writeback during active resizing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shenruiyang/skills/orbcafe-agentui-chat)
- [Component Selection](references/component-selection.md)
- [AgentUI Guardrails](references/guardrails.md)
- [AgentUI Recipes](references/recipes.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with TypeScript/TSX and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes component choice, minimal code, state shape, verification steps, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
