## Description: <br>
Provides macOS text-to-speech guidance using the built-in `say` command for spoken notifications, alerts, reading text aloud, and multilingual voice selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kalijason](https://clawhub.ai/user/kalijason) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users on macOS use this skill to have an agent provide local text-to-speech and volume-control commands for notifications, reminders, alerts, and reading short messages aloud. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make the Mac speak through local speakers and includes commands that adjust or unmute system volume. <br>
Mitigation: Use it only when audible output is appropriate, and review any volume-related commands before running them. <br>
Risk: The documented commands depend on macOS-specific tools. <br>
Mitigation: Treat the skill as macOS-only and check the operating system before using generated commands. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with bash command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [macOS-only commands that may run synchronously unless invoked in the background.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
