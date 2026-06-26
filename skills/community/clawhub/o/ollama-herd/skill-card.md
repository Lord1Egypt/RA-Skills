## Description: <br>
Ollama Herd helps agents inspect, route, and manage local Ollama fleet inference, model, dashboard, health, and analytics workflows across macOS, Linux, and Windows devices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to monitor an Ollama Herd router, check fleet and node health, inspect model availability and request traces, and prepare curl commands for local inference and model management actions. It is intended for self-hosted Ollama environments where disruptive actions require explicit user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Model pulls, deletes, settings changes, restarts, and stops can consume significant disk space or alter local fleet behavior. <br>
Mitigation: Require explicit user approval before performing these actions. <br>
Risk: Router and node agents expose local fleet services and diagnostics. <br>
Mitigation: Run them only on trusted devices and networks, and verify the PyPI package and linked repository before installation. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/twinsgeeks/ollama-herd) <br>
- [PyPI package](https://pypi.org/project/ollama-herd/) <br>
- [Project homepage](https://github.com/geeks-accelerator/ollama-herd) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and API endpoint examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local router endpoints, local configuration paths, and local SQLite or JSONL diagnostics.] <br>

## Skill Version(s): <br>
1.5.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
