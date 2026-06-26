## Description: <br>
Warm multi-turn goal clarification and action planning. Use when the user has a vague, oversized, or tangled goal and wants help thinking it through, narrowing focus, or turning it into concrete next steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terryxdguan](https://clawhub.ai/user/terryxdguan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and employees use this skill to clarify vague or oversized goals, explore constraints, choose a realistic focus, and turn the result into concrete next steps or weekly plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Goal progress, weekly plans, and user notes can contain sensitive personal or work context. <br>
Mitigation: Avoid including highly sensitive details unless they are necessary for planning, and review the context supplied to the agent. <br>
Risk: Generated weekly plans may be unsuitable if the supplied constraints or progress context are incomplete. <br>
Mitigation: Review any weeklyPlan JSON and adjust it against the user's real time, energy, commitments, and task priorities before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terryxdguan/goal-clarifier) <br>
- [English guide](references/guide-en.md) <br>
- [Chinese guide](references/guide-zh.md) <br>
- [English workflow](references/workflow-en.md) <br>
- [Chinese workflow](references/workflow-zh.md) <br>
- [English examples](references/examples-en.md) <br>
- [Chinese examples](references/examples-zh.md) <br>
- [English evaluation checklist](references/eval-checklist-en.md) <br>
- [Chinese evaluation checklist](references/eval-checklist-zh.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown conversation responses; weekly schedules may be emitted as JSON code blocks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responds in the user's language and uses provided goal context as background when available.] <br>

## Skill Version(s): <br>
0.6.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
