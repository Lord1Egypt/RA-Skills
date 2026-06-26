## Description: <br>
Operate Shortcut through the OOMOL `oo` CLI to read, create, and update Shortcut workspace data without handling raw API tokens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace operators use this skill to inspect Shortcut action schemas, read project planning data, and prepare confirmed story or epic changes through OOMOL-connected Shortcut accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or update Shortcut stories and epics. <br>
Mitigation: Inspect the live action schema and confirm the exact payload and expected effect before running write actions. <br>
Risk: The skill requires connected Shortcut credentials through OOMOL. <br>
Mitigation: Use an intended OOMOL account and only reconnect Shortcut when an auth or connection error requires it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-shortcut) <br>
- [OOMOL Publisher Profile](https://clawhub.ai/user/oomol) <br>
- [Shortcut Homepage](https://www.shortcut.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Actions may return JSON data with execution metadata when run through the oo CLI.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
