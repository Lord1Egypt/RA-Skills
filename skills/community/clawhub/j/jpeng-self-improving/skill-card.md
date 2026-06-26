## Description: <br>
Self-reflection + Self-criticism + Self-learning + Self-organizing memory. Agent evaluates its own work, catches mistakes, and improves permanently. Use before starting work and after responding to the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to help an agent learn from explicit corrections, self-reflection, and repeated workflow patterns while keeping those lessons in local memory files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores durable local memory that can influence future agent behavior. <br>
Mitigation: Enable it only when durable memory is desired, require confirmation before the first write, and periodically inspect or delete ~/self-improving/. <br>
Risk: User-derived data could include sensitive or inappropriate memory entries. <br>
Mitigation: Do not store secrets, financial or medical data, location routines, third-party details, or sensitive work context; follow the artifact's security boundaries. <br>
Risk: Deletion and export behavior is under-scoped without explicit review. <br>
Mitigation: Require confirmation before deletion or export operations and verify the updated memory state after removal. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/jpeng-self-improving) <br>
- [Skill homepage](https://clawic.com/skills/self-improving) <br>
- [Security boundaries](artifact/boundaries.md) <br>
- [Setup guide](artifact/setup.md) <br>
- [Memory operations](artifact/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local memory files under ~/self-improving/ when the user enables the workflow.] <br>

## Skill Version(s): <br>
1.2.11 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
