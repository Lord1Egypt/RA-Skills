## Description: <br>
Cross-platform local printer CLI - Manage and print to local printers (Windows/macOS/Linux) via the printer-ai CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NullYing](https://clawhub.ai/user/NullYing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to list local printers, check printer status and attributes, print local files, and inspect or cancel print jobs through the printer-ai CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to submit or cancel local print jobs, which may produce unintended physical output or affect active printer queues. <br>
Mitigation: Confirm the target printer, file path, job id, and print options with the user before running printer-ai print or cancel-job commands. <br>
Risk: Future versions could change the local risk profile if they add dependencies, network access, file access, credential handling, or broader commands. <br>
Mitigation: Review future versions and their security evidence before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/NullYing/printer-ai-skills) <br>
- [printer-ai install package](https://github.com/NullYing/printer-ai-skills.git) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON option examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference platform-specific print option formats for Windows, macOS, and Linux.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
