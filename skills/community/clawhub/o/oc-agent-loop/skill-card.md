## Description: <br>
Keep OpenClaw maintenance tight: diagnose one issue, change one thing, validate it, then keep or revert with evidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiepu110](https://clawhub.ai/user/jiepu110) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to keep local OpenClaw maintenance work bounded, evidence-backed, and reviewable while diagnosing issues, making small candidate changes, validating them, and deciding whether to keep, revise, or revert. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Specialized maintainer workflows can affect production systems when used outside a trusted maintainer environment. <br>
Mitigation: Use the skill only in a trusted ClawHub maintainer environment and review changes carefully before installing or applying them. <br>
Risk: Autoreview workflows may grant nested Codex more filesystem and command authority than routine review requires. <br>
Mitigation: Prefer running autoreview with --no-yolo or AUTOREVIEW_YOLO=0 unless full authority is intentional. <br>
Risk: Agent-assisted maintenance can drift into broad or unvalidated changes. <br>
Mitigation: Keep work to one narrow issue, cap iterations, run targeted validation, and revert candidate changes when validation is missing or failing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiepu110/oc-agent-loop) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with concise change summaries, validation summaries, decisions, and follow-up items] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bounded local maintenance loop with an explicit keep, revise, or revert decision.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
