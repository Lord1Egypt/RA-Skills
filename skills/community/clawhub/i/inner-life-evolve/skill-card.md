## Description: <br>
Inner Life Evolve analyzes an agent's patterns, challenges assumptions, and writes reviewable improvement proposals to the task queue without auto-executing them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DKistenev](https://clawhub.ai/user/DKistenev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to review recurring agent behavior, identify stale patterns or assumptions, and queue concrete self-improvement proposals for human approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local memory and core agent instruction files to generate improvement proposals. <br>
Mitigation: Install only if this local context access is acceptable, and keep the reviewed memory and instruction files scoped to the intended agent environment. <br>
Risk: Queued self-improvement proposals could be incorrect, unsuitable, or misleading if accepted without review. <br>
Mitigation: Treat [EVOLVER] entries as suggestions that require user approval, and review any resulting changes before deployment. <br>
Risk: The required inner-life-core setup may involve running an initialization script. <br>
Mitigation: Review inner-life-core's init.sh before running it and verify the required files exist before using this skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DKistenev/inner-life-evolve) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown task queue entries and a short natural-language summary; may include shell commands for missing prerequisites.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires jq and initialized inner-life-core files; writes reviewable proposals to tasks/QUEUE.md only.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
