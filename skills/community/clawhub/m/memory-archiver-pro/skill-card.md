## Description:

Automatically archives AI agent memory files by date, supports keyword search and cross-session memory inheritance, and generates daily memory briefings to reduce information loss.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linbo405](https://clawhub.ai/user/linbo405)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw Agent users use this skill to organize memory files into dated archives, search prior context, continue work across sessions, and produce daily summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and summarize memory files, which may carry private or sensitive information across sessions.

Mitigation: Use a narrow archive directory and avoid storing secrets or private data in memory files.

Risk: Automatic cleanup can delete memory records older than the configured retention period.

Mitigation: Disable auto-clean unless backups exist and review the retention period before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linbo405/skills/memory-archiver-pro)

## Skill Output:

**Output Type(s):** [Files, Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown or text summaries, search-result lists, archived knowledge-base files, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May process files under the configured memory archive and may remove expired records when auto-clean is enabled.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
