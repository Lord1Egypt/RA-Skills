## Description: <br>
Detects wake words in speech and routes voice commands like email, text, reminders, search, calendar, and notes to OpenClaw agents for execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jarvis563](https://clawhub.ai/user/jarvis563) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to configure hands-free OpenClaw control through wake words, authorized speakers, and supported actions such as messages, reminders, search, calendar queries, notes, and custom commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ambient speech can trigger OpenClaw actions through wake words and command routing. <br>
Mitigation: Install only when voice control is intended, use distinctive wake words, and avoid shared or noisy environments. <br>
Risk: Voice commands may reach broad OpenClaw CLI actions without enough documented safeguards. <br>
Mitigation: Require explicit approval for high-risk commands and verify how to pause listening, inspect logs, and disable or remove the skill. <br>
Risk: Commands from unapproved speakers may still be captured and logged. <br>
Mitigation: Configure approved speakers before use and review logs for unexpected or unwanted captured commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jarvis563/percept-voice-cmd) <br>
- [Percept GitHub repository](https://github.com/GetPercept/percept) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with configuration paths and command-routing behavior] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Describes wake word setup, supported actions, speaker authorization, contact resolution, and OpenClaw CLI dispatch behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
