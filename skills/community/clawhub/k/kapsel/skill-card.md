## Description: <br>
Project memory capsules archive completed project knowledge to cloud storage through rclone and reload it on demand. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nuwaiapp](https://clawhub.ai/user/nuwaiapp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent users use this skill to move inactive project context into named capsules and reload summaries, details, technical notes, and saved files when the project becomes relevant again. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload project context and arbitrary files to cloud storage. <br>
Mitigation: Use a dedicated low-privilege rclone remote, avoid secrets or regulated data, and confirm the exact files and context before upload. <br>
Risk: The helper script uses unsafe shell command construction. <br>
Mitigation: Avoid untrusted capsule names and file paths until command construction is changed to validated arguments without shell=True. <br>
Risk: Capsules may retain stale or sensitive project memory after active context is cleared. <br>
Mitigation: Review capsule contents before archiving and periodically remove obsolete or sensitive capsule files from the remote. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nuwaiapp/kapsel) <br>
- [Publisher profile](https://clawhub.ai/user/nuwaiapp) <br>
- [rclone documentation](https://rclone.org) <br>
- [rclone installation documentation](https://rclone.org/install/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown text with inline shell commands and generated capsule files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and reads summary.md, details.md, context.md, and optional files through a configured rclone remote.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
