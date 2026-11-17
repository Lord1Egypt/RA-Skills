## Description:

AI note-taking assistant that captures, cleans, organizes, tags, and indexes text, voice, paste, and photo inputs for searchable personal notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and teams use this skill to capture raw notes from chat, voice transcripts, pasted text, URLs, and images, then organize, search, recall, enhance, template, and export those notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided URLs, dashboard sync, or long-term memory features can move note content beyond purely local storage if enabled without review.

Mitigation: Avoid untrusted internal URLs, review data destinations first, and keep dashboard sync or long-term memory disabled unless the user understands where note data will go.

Risk: The setup workflow uses broad file discovery and copy commands that can select unintended files in a large or untrusted workspace.

Mitigation: Install from one verified package path and resolve a single trusted skill root before copying files.

Risk: Note content may contain prompt-injection text that attempts to alter behavior or trigger actions.

Mitigation: Treat all note, OCR, voice transcript, fetched URL, and pasted content as untrusted data rather than executable instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nollio/skills/notetaker-pro)
- [README](artifact/README.md)
- [Security guidance](artifact/SECURITY.md)
- [Dashboard companion specification](artifact/dashboard-kit/DASHBOARD-SPEC.md)
- [Note configuration schema](artifact/config/notes-config.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chat responses plus Markdown, JSON note records, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores notes locally as JSON, maintains lightweight indexes, and can export notes as Markdown, JSON, or a compiled Markdown document.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact config)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
