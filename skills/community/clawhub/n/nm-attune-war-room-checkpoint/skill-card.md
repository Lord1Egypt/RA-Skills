## Description: <br>
Assesses decision reversibility and risk at critical checkpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent workflow authors use this embedded checkpoint skill to assess reversibility, risk, and escalation needs before continuing high-stakes implementation or review decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local checkpoint and decision records may include project details. <br>
Mitigation: Use the skill in a protected workspace, review configured storage paths, and periodically delete or redact audit records that should not be retained. <br>


## Reference(s): <br>
- [Attune plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/attune) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown with structured checkpoint fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a reversibility score, selected escalation mode, recommendation or orders, confidence, and user confirmation flag.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
