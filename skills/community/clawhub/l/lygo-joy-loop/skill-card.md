## Description: <br>
Runs local LYGO Joy Loop tasks in a lygo-protocol-stack checkout with scoped writes, explicit activation triggers, and consent gates for state-changing commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deepseekoracle](https://clawhub.ai/user/deepseekoracle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators who already use the LYGO protocol stack can use this skill to inspect Joy Loop state, run local ticks, start local dashboard flows, or perform consent-gated plant actions while keeping writes scoped to the stack checkout. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local tick and runtime commands can write Joy Loop state and update docs/joy_loop/joy_loop_snapshot.json. <br>
Mitigation: Confirm LYGO_STACK_ROOT first, state the command tier, and tell the user which files may change before running write commands. <br>
Risk: The Joy Loop snapshot can become world-readable if the user later pushes the repository to GitHub Pages. <br>
Mitigation: Warn the user before snapshot-updating commands when a push is plausible, and do not run git push or publish steps unless the user explicitly asks. <br>
Risk: Plant actions can mutate registry-related Joy Loop state. <br>
Mitigation: Require explicit user consent, use the --i-consent path, and do not set LYGO_JOY_PLANT_CONSENT unless the user has said they consent. <br>
Risk: Interactive dashboard or serve modes can expose a local service. <br>
Mitigation: Run local network flows only when requested and keep them bound to 127.0.0.1 unless the user explicitly asks for another binding. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/deepseekoracle/skills/lygo-joy-loop) <br>
- [LYGO protocol stack repository](https://github.com/DeepSeekOracle/lygo-protocol-stack) <br>
- [Security and disclosure](references/SECURITY.md) <br>
- [Agent contract](references/AGENT_CONTRACT.md) <br>
- [JoyLoopRegistry public mirror](https://deepseekoracle.github.io/lygo-protocol-stack/JoyLoopRegistry.json) <br>
- [Joy Loop snapshot public mirror](https://deepseekoracle.github.io/lygo-protocol-stack/joy_loop/joy_loop_snapshot.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are tiered by risk and must remain scoped to LYGO_STACK_ROOT with consent for write, serve, plant, or publish actions.] <br>

## Skill Version(s): <br>
2.3.1 (source: SKILL.md metadata and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
