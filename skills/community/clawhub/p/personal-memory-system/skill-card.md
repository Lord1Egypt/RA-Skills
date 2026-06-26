## Description: <br>
Personal AI Memory System is a local-first memory skill that helps an AI assistant record journals, maintain a personal profile, track goals, review past experiences, and support decision analysis from user-provided history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenchen913](https://clawhub.ai/user/chenchen913) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users use this skill to build a private personal memory workspace for journaling, reflection, goal tracking, periodic reports, and decision support with their chosen AI assistant. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores intimate personal history, diary entries, goals, and behavioral signals in a local memory directory. <br>
Mitigation: Use a dedicated memory directory with restricted permissions, keep it out of git and unintended cloud sync, and consider encrypted storage. <br>
Risk: Relevant diary or memory content may be sent to the selected AI provider as conversation context during use. <br>
Mitigation: Use explicit trigger phrases, choose an AI provider with acceptable data-retention terms, and avoid submitting content that should not leave the device. <br>
Risk: Long-running memory files may accumulate sensitive or outdated personal data. <br>
Mitigation: Periodically inspect, edit, archive, or delete profile, diary, signal, report, and AI-portrait files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chenchen913/personal-memory-system) <br>
- [Project homepage](https://github.com/ChenChen913/memory-system) <br>
- [Initialization flow](references/00-initialization.md) <br>
- [Present dimension spec](references/01-present.md) <br>
- [Past dimension spec](references/02-past.md) <br>
- [Future dimension spec](references/03-future.md) <br>
- [Special protocols](references/05-protocols.md) <br>
- [AI voice specification](references/06-ai-voice.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with local file paths and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local memory files only after explicit user-triggered use.] <br>

## Skill Version(s): <br>
3.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
