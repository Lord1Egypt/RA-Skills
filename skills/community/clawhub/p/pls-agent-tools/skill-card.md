## Description: <br>
Provides command references for file handling, JSON/YAML/TOML editing, regex text processing, system utilities, encoding, date/time, and validation tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mattvalenta](https://clawhub.ai/user/mattvalenta) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill as a quick reference for everyday utility tasks, including safe file operations, structured-data editing, text processing, process checks, network checks, encoding, time conversion, and validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes examples for deleting, moving, copying, and editing files, which can change or remove local data if applied to the wrong path. <br>
Mitigation: Confirm the exact target path and expected effect before executing file-changing commands, and prefer recoverable deletion where available. <br>
Risk: The skill includes examples for killing processes, downloading files, and sending network requests, which can interrupt services or contact unintended endpoints. <br>
Mitigation: Confirm the process name, port, URL, request method, payload, and expected operational impact before executing these commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mattvalenta/pls-agent-tools) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown reference material with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may affect files, processes, or network endpoints; review exact targets before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
