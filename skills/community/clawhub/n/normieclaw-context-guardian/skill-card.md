## Description: <br>
Context Guardian helps agents manage long-running conversations by tracking session health, prompting for fresh starts, and saving important notes to workspace memory files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nollio](https://clawhub.ai/user/nollio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, employees, and external agent users use this skill to keep long sessions organized, preserve decisions and preferences, and recover context through local workspace notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Always-on local memory can preserve conversation details or preferences longer than the user expects. <br>
Mitigation: Decide whether silent saves are acceptable before use, review generated memory files periodically, and avoid storing secrets or sensitive personal details. <br>
Risk: The skill may create or load local notes during future sessions. <br>
Mitigation: Use a dedicated workspace memory directory and instruct the agent to ask before saving or loading notes when tighter control is required. <br>


## Reference(s): <br>
- [Context Guardian setup guide](references/setup-guide.md) <br>
- [ClawHub skill release page](https://clawhub.ai/nollio/normieclaw-context-guardian) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional shell commands and local note files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local memory files when the agent follows the skill.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
