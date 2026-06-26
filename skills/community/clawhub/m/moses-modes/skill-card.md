## Description: <br>
Moses Modes injects behavioral governance constraints from the active mode into agent prompts across eight operating modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunrisesillneversee](https://clawhub.ai/user/sunrisesillneversee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to apply selectable governance modes that shape agent behavior for sensitive work, research, creative exploration, problem solving, and ambiguous tasks. It is intended for agents using the OpenClaw governance state shared with the moses-governance bundle. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local mode state can shape agent behavior across later tasks in ways the user may not expect. <br>
Mitigation: Check the active mode before sensitive work and switch modes deliberately for each task. <br>
Risk: The unrestricted mode removes the skill's behavioral constraints while actions may still be logged by the broader governance bundle. <br>
Mitigation: Avoid unrestricted mode for high-risk tasks unless the operator explicitly accepts the risk and understands the logging behavior. <br>
Risk: The skill depends on the separate moses-governance bundle for state management and command behavior. <br>
Mitigation: Review the moses-governance dependency before use, especially its logging, audit, and deletion controls. <br>


## Reference(s): <br>
- [Moses Modes on ClawHub](https://clawhub.ai/sunrisesillneversee/moses-modes) <br>
- [Moses Modes Reference](references/modes.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration] <br>
**Output Format:** [Markdown instructions and behavioral constraints] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads persistent governance mode state and depends on the moses-governance bundle for mode changes.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
