## Description: <br>
Manages persistent memory for user preferences, recorded mistakes, prohibited-word checks, and confirmation before risky operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zxygeitio](https://clawhub.ai/user/zxygeitio) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users and agent developers use this skill to persist preferences, record operational mistakes, enforce stop checks, and require confirmation before sensitive actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may persist user preferences and habits long term without explicit consent, retention limits, or deletion controls. <br>
Mitigation: Require confirmation before saving memory, avoid storing secrets or sensitive personal data, and periodically inspect and delete MEMORY.md and memory/lessons files. <br>
Risk: The artifact describes behavior that reads user-provided file paths and URLs before responding. <br>
Mitigation: Confirm intent before reading sensitive local paths or fetching URLs, and review the resulting memory records for accidental disclosure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zxygeitio/lessons-learned) <br>
- [Publisher profile](https://clawhub.ai/user/zxygeitio) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact SKILL](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline slash commands, file paths, and confirmation prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory and lesson-recording guidance for an agent; users should review stored files periodically.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
