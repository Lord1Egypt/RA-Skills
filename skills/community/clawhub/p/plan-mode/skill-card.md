## Description: <br>
Think-first execution with approval gating for complex, ambiguous, irreversible, multi-step, comparative, interrupted, or long-running agent work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pieterjanliekens](https://clawhub.ai/user/pieterjanliekens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to make an agent inspect context, compare options, produce an approval-gated plan, and recover or maintain continuity for complex work before making changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may add planning overhead when used for work that is simple or already clear. <br>
Mitigation: It instructs the agent not to force planning for trivial edits, simple factual questions, obvious follow-up actions, or requests where the user disables planning. <br>
Risk: Persistent planning records may expose project details if created too early. <br>
Mitigation: It requires explicit user approval before creating or updating living-plan files. <br>
Risk: External toolbox or registry lookups may disclose private project context. <br>
Mitigation: It requires a local-first toolbox audit and user approval before external registry searches. <br>
Risk: Plans can still contain incorrect, incomplete, or misleading guidance. <br>
Mitigation: It keeps planning read-only until approval and requires checkpoints, approval asks, and pausing when new information changes risk or recommendations. <br>


## Reference(s): <br>
- [Plan Mode ClawHub page](https://clawhub.ai/pieterjanliekens/plan-mode) <br>
- [Plan Mode Patterns Across AI Tools](references/patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance with structured planning sections and approval prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Planning stance is read-only until approval; persistent plan files require explicit user approval.] <br>

## Skill Version(s): <br>
3.0.4 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
