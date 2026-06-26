## Description: <br>
Classifies personal computer operations by security risk level and helps agents assess local and browser actions using the PC-OCS v1.0 rubric. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huaiyu](https://clawhub.ai/user/huaiyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to classify requested PC operations into L1-L4 risk levels, explain the likely impact, and recommend safeguards before local, browser, identity, data, system, finance, or communication actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Risk ratings are advisory and may over- or under-classify ambiguous operations because the helper script uses simple keyword matching. <br>
Mitigation: Review the operation context manually, prefer the higher risk level when uncertainty remains, and do not treat the shell helper as an authoritative security decision system. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance and optional shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Risk assessments include operation description, L1-L4 level, rationale, recommended safeguards, and related high-risk scenarios.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
