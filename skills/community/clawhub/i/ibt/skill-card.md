## Description: <br>
Execution discipline for agents with instinct, verification, trust calibration, approval gates, trust boundaries, trust recovery, discrepancy reasoning, resilient error handling, and preference learning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[palxislabs](https://clawhub.ai/user/palxislabs) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use IBT to guide agents through multi-step or trust-sensitive work with calibrated autonomy, approval gates, verification, recovery behavior, and human-editable preference memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Preference memory in USER.md may retain stale, overly specific, or personal entries. <br>
Mitigation: Review USER.md periodically, delete stale or personal entries, and keep stored preferences generic and task-relevant. <br>
Risk: Implicit preferences could affect future agent behavior without clear user intent. <br>
Mitigation: Persist implicit or learned preferences only after clear user agreement, and allow the user to view, edit, or delete them at any time. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/palxislabs/ibt) <br>
- [README.md](artifact/README.md) <br>
- [POLICY.md](artifact/POLICY.md) <br>
- [EXAMPLES.md](artifact/EXAMPLES.md) <br>
- [TEMPLATE.md](artifact/TEMPLATE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance and policy templates for agent behavior] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; no API calls, commands, external services, or executable code are provided by the artifact.] <br>

## Skill Version(s): <br>
2.9.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
