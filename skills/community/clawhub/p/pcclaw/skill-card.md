## Description:

PCClaw provides 16 OpenClaw skills for Windows system control, automation, files, notifications, OCR, speech, local LLM inference, browser access, scheduling, and task management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lmanchu](https://clawhub.ai/user/lmanchu)

### License/Terms of Use:

MIT

## Use Case:

External Windows users and developers use PCClaw to add Windows-native OpenClaw abilities for automation, local system inspection, file and clipboard workflows, screenshots, OCR, speech, local AI, browser data access, scheduling, and task management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer and skills can grant broad Windows automation and sensitive local data access.

Mitigation: Review proposed commands before execution and approve browser history, clipboard, screenshot/OCR, microphone, filesystem, package, UI automation, and scheduled-task actions only when explicitly requested.

Risk: The quick-start path executes a remote installer.

Mitigation: Review the remote installer first or use the manual skill-copy path.

Risk: Task-management workflows can rely on OAuth refresh tokens.

Mitigation: Store refresh tokens carefully and revoke them if exposed.

Risk: Scheduled-task and PATH changes can persist after use.

Mitigation: Periodically inspect and remove unwanted PCClaw scheduled tasks and PATH changes.

## Reference(s):

- [PCClaw README](artifact/README.md)
- [PCClaw Changelog](artifact/CHANGELOG.md)
- [PCClaw ClawHub Page](https://clawhub.ai/lmanchu/skills/pcclaw)
- [PCClaw Website](https://openclaw.irisgo.xyz)
- [OpenClaw Official](https://openclaw.ai)
- [whisper.cpp](https://github.com/ggml-org/whisper.cpp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline PowerShell, shell, JSON, REST API, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target Windows PowerShell plus selected cross-platform REST and CLI workflows.]

## Skill Version(s):

2.0.0 (source: release evidence and CHANGELOG, released 2026-02-12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
