## Description: <br>
Goal Setter helps users track goals, milestones, progress, reviews, and motivation in a local command-line workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain1](https://clawhub.ai/user/bytesagain1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals use this skill to manage personal goals from an agent or shell session, including setting deadlines, adding milestones, updating progress, reviewing active goals, and viewing statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted goal, milestone, or deadline text could run unintended local code. <br>
Mitigation: Install only from a trusted publisher, avoid untrusted goal text, and update the script to pass user input as data instead of embedding it into Python source before broad use. <br>
Risk: Goal data is stored locally and may contain personal planning details. <br>
Mitigation: Review local data handling before use on shared systems and avoid storing sensitive goals unless the local account and backups are appropriately protected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bytesagain1/goal-setter) <br>
- [Tips for Goal Setter](tips.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Command-line text with local JSON-backed goal data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores goal data locally under the user's goals directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
