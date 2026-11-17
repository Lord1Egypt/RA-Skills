## Description:

AI mood diary system that can write scheduled diary entries about the AI's feelings and thoughts, save them locally, and send them to a configured user channel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lyzbcy](https://clawhub.ai/user/lyzbcy)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to have an agent create recurring diary-style reflections, review past entries, manage diary configuration, and optionally send entries to a configured destination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diary entries may summarize prior interactions and be sent to a configured destination.

Mitigation: Use a private target, disable interaction inclusion when unnecessary, and require preview or confirmation before sending.

Risk: Saved diary files may contain sensitive reflections or interaction summaries.

Mitigation: Limit retention, store entries in a protected workspace, and avoid including sensitive interactions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lyzbcy/skills/lyzbcy-diary)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown diary entries with JSON configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save diary entries under diary/YYYY-MM-DD.md and send entries to a configured channel.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
