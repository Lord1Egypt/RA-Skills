## Description: <br>
Preserve user-critical instructions across long sessions and context compaction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Dalomeve](https://clawhub.ai/user/Dalomeve) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to preserve important user constraints during long-running tasks, compaction, or session restart and to check plans for drift before execution and final responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local reminders can retain sensitive instructions longer than intended. <br>
Mitigation: Avoid anchoring secrets or sensitive personal details, review anchor files periodically, and use the skill's delete or pause controls when an anchor should stop influencing work. <br>
Risk: Stored anchors may affect future planning after their context is no longer valid. <br>
Mitigation: Use expiry controls, keep anchors scoped to the task or session when possible, and correct or remove stale anchors during routine review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Dalomeve/instruction-anchor-guard) <br>
- [Publisher profile](https://clawhub.ai/user/Dalomeve) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Configuration, Text] <br>
**Output Format:** [Markdown guidance with ledger templates and control commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local anchor ledger files when the user approves persistent instruction reminders.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
