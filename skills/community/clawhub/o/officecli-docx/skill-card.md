## Description: <br>
Guides agents through reading, creating, editing, and validating .docx documents with OfficeCLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iceyliu](https://clawhub.ai/user/iceyliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and agents use this skill to inspect, create, modify, and quality-check Microsoft Word .docx files with OfficeCLI command workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan says normal use may download and run an unpinned OfficeCLI installer or updater from GitHub. <br>
Mitigation: Install only after trusting the OfficeCLI upstream installer; prefer a pinned, verified OfficeCLI version installed separately. <br>
Risk: Bulk tracked-change, global replace, remove, or raw XML commands can damage or mis-edit important documents. <br>
Mitigation: Run the skill only for explicit .docx work, edit copies of important documents, and review validation output before delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iceyliu/officecli-docx) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, text, markdown, configuration] <br>
**Output Format:** [Markdown guidance with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May result in .docx file creation or edits when the agent executes OfficeCLI commands.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
