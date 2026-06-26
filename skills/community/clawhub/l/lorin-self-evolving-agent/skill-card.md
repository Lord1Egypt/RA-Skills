## Description: <br>
A self-improvement skill that helps an agent capture command errors, record user corrections and learned workflows, and extract recurring learnings into reusable skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lorinwei](https://clawhub.ai/user/lorinwei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to maintain structured learning logs, review repeated issues, and convert verified recurring workflows into reusable agent skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent self-improvement behavior can write learned guidance into future agent context. <br>
Mitigation: Keep hooks project-scoped where possible and require manual review before promoting learnings into persistent prompt or skill files. <br>
Risk: Learning logs may capture sensitive context from errors, commands, or user feedback. <br>
Mitigation: Redact secrets and raw command output before storing learnings or sharing summaries across sessions. <br>
Risk: Deletion or replacement of stale skills can remove useful local knowledge. <br>
Mitigation: Use backup or trash-based removal instead of direct deletion when retiring generated skill files. <br>


## Reference(s): <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Entry Examples](references/examples.md) <br>
- [Skill Template](assets/SKILL-TEMPLATE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and skill templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local learning logs, skill files, and hook configuration when the operator chooses to enable those workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
