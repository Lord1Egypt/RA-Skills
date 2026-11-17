## Description:

AI-powered note-taking assistant that captures, cleans, tags, organizes, indexes, searches, and exports text, voice, pasted, and photo notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

MIT

## Use Case:

External users and agent operators use this skill to capture, organize, search, enhance, and export personal or work notes from chat, voice transcriptions, pasted text, URLs, and photos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security claims understate network, memory, dashboard-sync, and third-party messaging exposure for sensitive notes.

Mitigation: Review before installing for sensitive use; disable URL fetching, memory integrations, dashboard sync, and third-party messaging channels unless the data flow is acceptable.

Risk: The export workflow may be unreliable until the included shell script is fixed and tested.

Mitigation: Treat exports as unavailable for backups or migrations until the script passes shell syntax checks and functional tests on representative note data.

Risk: Prompt injection in notes, OCR text, transcripts, pasted articles, or fetched URLs could attempt to change agent behavior or trigger unsafe actions.

Mitigation: Keep ingested content as untrusted data, ignore command-like note content, and review agent actions before file writes, tool use, or external integrations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nollio/skills/normieclaw-notetaker-pro)
- [Publisher profile](https://clawhub.ai/user/nollio)
- [README.md](artifact/README.md)
- [SECURITY.md](artifact/SECURITY.md)
- [DASHBOARD-SPEC.md](artifact/dashboard-kit/DASHBOARD-SPEC.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and structured note JSON, with optional shell commands for setup and export workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Captures note metadata, tags, categories, action items, search previews, export files, and optional dashboard sync specifications.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
