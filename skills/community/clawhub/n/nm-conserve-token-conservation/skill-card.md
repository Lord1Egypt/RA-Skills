## Description: <br>
Enforces token quota management at session start with conservation and compression checks before large context loads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to keep long coding or investigation sessions within a planned context budget. It guides quota checks, read budgeting, delegation decisions, compression review, and concise logging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Frequent use in ordinary sessions can distract from the task or waste context. <br>
Mitigation: Invoke it for large-context planning, long investigations, or sessions where context budget is already a concern. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-conserve-token-conservation) <br>
- [Clawdis homepage](https://github.com/athola/claude-night-market/tree/master/plugins/conserve) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with concise checklists and next-action lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend starting a new session or compacting conversation context when the context budget is low.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
