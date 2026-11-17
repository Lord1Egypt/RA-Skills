## Description:

Music Tagger provides a Python CLI framework for previewing and organizing local music files and simulating read, edit, and batch metadata operations.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[utopiabenben](https://clawhub.ai/user/utopiabenben)

### License/Terms of Use:

MIT License

## Use Case:

Developers and music-library users can use this skill to run or adapt a local command-line workflow for inspecting, previewing, batch tagging, and organizing music files by artist, album, genre, or year. Current artifact behavior is best treated as a prototype because tag read/write operations are simulated.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact may overstate music tag editing capabilities because current tag read/write behavior is simulated.

Mitigation: Treat the skill as a prototype and verify behavior on test copies before using it with a real music library.

Risk: Undo and backup handling can copy or delete unintended local files if backup data is tampered with.

Mitigation: Use preview mode first, avoid shared or untrusted output directories, and rely on undo only when the backup file is trusted.

Risk: Optional dependencies can affect local file handling behavior.

Mitigation: Pin and review dependencies before installation.

## Reference(s):

- [Music Tagger README](artifact/README.md)
- [ClawHub Skill Page](https://clawhub.ai/utopiabenben/skills/music-tagger)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or copy local music files when organize or undo actions are executed outside preview mode.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
