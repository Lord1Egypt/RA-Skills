## Description:

Update freznel's Obsidian daily note with timestamped activity entries, especially day recaps, travel logs, itineraries, movement updates, and "I did X at Y time" messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freznel10](https://clawhub.ai/user/freznel10)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal automation agents use this skill to turn natural-language day recaps, travel logs, errands, and activity updates into timestamped Obsidian daily-note timeline entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The updater can be steered to modify Markdown files outside the intended daily-notes folder if unsafe path arguments are supplied.

Mitigation: Review before installing, validate dates, and constrain writes to the configured daily-notes directory before using the updater.

Risk: Shared-chat messages may cause unintended personal note updates if intent is ambiguous.

Mitigation: Require clear logging triggers or ask for confirmation before saving entries from group-chat contexts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freznel10/skills/obsidian-daily-log)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown timeline entries with optional shell command invocation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes chronological bullets by default; can produce a table when requested or when entries are highly structured.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
