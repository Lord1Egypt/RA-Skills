## Description: <br>
Helps agents create structured context handoffs when switching models or agents so task history, status, constraints, decisions, and next steps carry forward. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lujun2508](https://clawhub.ai/user/lujun2508) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to summarize an ongoing task before switching models or handing work to another agent. The handoff captures project background, progress, blockers, constraints, decisions, file paths, tools, team roles, warnings, and next steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Context handoffs may include credentials, customer data, private file contents, or other sensitive details. <br>
Mitigation: Redact tokens, passwords, customer data, private file contents, and unnecessary file paths before sharing a handoff; share summaries only with trusted models or agents. <br>
Risk: A receiving model or agent may rely on incomplete, stale, or misleading task status captured in a handoff. <br>
Mitigation: Review the generated handoff before use and confirm current blockers, constraints, decisions, and next steps with the user when accuracy matters. <br>


## Reference(s): <br>
- [Quick Transfer Template](artifact/references/quick-transfer-template.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/lujun2508/model-context-transfer) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Guidance] <br>
**Output Format:** [Markdown CONTEXT_TRANSFER handoff text or a context_transfer.md file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include task status, completed work, in-progress work, pending items, blockers, key decisions, constraints, file paths, tools, team roles, next steps, and warnings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
