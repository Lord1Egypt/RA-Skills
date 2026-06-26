## Description: <br>
Organizes local agent memory by detecting duplicate, outdated, conflicting, orphaned, fragmented, or oversized entries and producing an approval-gated cleanup proposal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jofiction918](https://clawhub.ai/user/jofiction918) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users who maintain local MEMORY.md, topics, and daily memory notes use this skill to audit memory hygiene and apply approved cleanup changes. It helps keep long-term memory concise, current, internally consistent, and backed by existing files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local memory and journal files that may contain sensitive personal or project information. <br>
Mitigation: Grant access only to the intended memory directories and review what the agent scans before sharing outputs. <br>
Risk: Cleanup proposals or approved edits could remove useful memories or encode an incorrect interpretation of current files. <br>
Mitigation: Review proposed changes before approval and keep normal backups or version control for memory files. <br>
Risk: Daily-journal write access broadens the files the agent can modify. <br>
Mitigation: Avoid granting daily-journal write access unless that broader permission is necessary and acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jofiction918/memory-sorting) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown checklist, cleanup proposal, and execution report; approved actions may edit local memory files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user approval before making cleanup edits.] <br>

## Skill Version(s): <br>
3.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
