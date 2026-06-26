## Description: <br>
Triage user-feedback issues in Linear, especially FB team / 用户反馈 workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qwqcode](https://clawhub.ai/user/qwqcode) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Support and product teams use this skill to query Linear feedback issues, identify duplicates, categorize membership or payment complaints, suggest labels and statuses, and draft concise user replies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent toward Linear write actions such as status, label, and comment updates. <br>
Mitigation: Review proposed Linear changes before execution and prefer read-only issue queries until a write is explicitly requested. <br>
Risk: Linear MCP credentials may expose team feedback data beyond the intended workflow. <br>
Mitigation: Configure credentials with access appropriate for the FB/Tide workflow and avoid installing the skill where that team data should not be read. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qwqcode/linear-feedback-triage) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries with Linear command examples and reply drafts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only queries are preferred before proposed Linear updates; write actions should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
