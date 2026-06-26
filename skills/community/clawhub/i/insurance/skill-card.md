## Description: <br>
Local-first insurance record organizer for tracking policy details, renewals, claims logs, and summary information without providing insurance advice or facilitating purchases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agenticio](https://clawhub.ai/user/agenticio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to organize locally stored insurance policy and claim records, list policies, check renewals, and summarize premiums. It is not for coverage recommendations, legal interpretation, or policy purchase decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Insurance records can include policy numbers, insured names, premiums, renewal dates, and claim notes in local workspace files. <br>
Mitigation: Use only in workspaces where local storage of these details is acceptable; manage retention and delete memory/insurance data when no longer needed. <br>
Risk: Users may treat summaries or missing categories as insurance, legal, or purchasing advice. <br>
Mitigation: Use outputs only to organize existing records; consult a licensed insurance professional for coverage decisions or legal interpretation. <br>
Risk: Local JSON records may be stale, incomplete, or inconsistent with official policy documents. <br>
Mitigation: Verify stored values against current policy documents before relying on renewal dates, premiums, claim notes, or coverage details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agenticio/insurance) <br>
- [Publisher profile](https://clawhub.ai/user/agenticio) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell-command invocations and JSON script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts store user-entered policy and claim records in local JSON files under memory/insurance/.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
