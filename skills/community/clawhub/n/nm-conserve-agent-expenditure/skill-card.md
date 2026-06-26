## Description: <br>
Tracks per-agent token usage and flags waste in parallel dispatch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill after multi-agent work to review token expenditure, duplicate effort, and coordination overhead. It helps decide whether future parallel dispatches should use fewer agents or clearer scopes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may need agent outputs or usage logs to assess waste. <br>
Mitigation: Provide only relevant outputs or logs, and avoid unrelated private project history. <br>
Risk: Waste classifications can be misleading when agent scopes, baselines, or findings are incomplete. <br>
Mitigation: Review the conclusions before changing dispatch patterns or agent-count policies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-conserve-agent-expenditure) <br>
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/conserve) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance and checklist-style analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Post-run review; may use relevant agent outputs or usage logs when available.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
