## Description:

Repairs garbled speech-to-text input by fixing mistranscribed names, numbers, commands, dictation markers, and recurring vocabulary in voice-dictated messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to repair voice-sourced transcripts before responding, acting on commands, or producing dictated artifacts. It is intended for text that already passed through speech-to-text, not for transcribing audio files or correcting typed typos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read or persist sensitive local correction data, including names, addresses, project identifiers, prior phrasing, and dictated terms.

Mitigation: Review the skill before installing and periodically inspect or delete ~/Clawic/data/listen/ when it contains sensitive or stale entries.

Risk: Incorrect voice repair can change recipients, amounts, dates, paths, branches, or other action targets.

Mitigation: Use strict confirmation for actions and confirm repaired values before side-effecting operations.

Risk: Persisted correction pairs can become stale and cause future misrepairs.

Mitigation: Prune old lexicon entries and keep active correction files small, following the documented lifecycle and TTL guidance.

## Reference(s):

- [Listen ClawHub release page](https://clawhub.ai/ivangdavila/skills/listen)
- [Listen homepage](https://clawic.com/skills/listen)
- [Clawic skill library](https://clawic.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text with repaired wording, confirmation prompts, dictated artifacts, code identifiers, shell commands, and configuration entries when applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist learned correction pairs and preferences under ~/Clawic/data/listen/.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
