## Description:

Use when the user mentions Otter, Otter.ai, or wants to find, search, download, export, or manage meeting notes, transcripts, recordings, or audio from calls, standups, syncs, or interviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erickhchan](https://clawhub.ai/user/erickhchan)

### License/Terms of Use:


## Use Case:

Developers and knowledge workers use this skill to operate the otter CLI for retrieving, searching, exporting, uploading, and organizing Otter.ai meeting transcripts, recordings, folders, speakers, and related metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an unpinned third-party CLI that handles Otter.ai account credentials and meeting content.

Mitigation: Install only from a trusted source, prefer a pinned and reviewed package version, use a trusted machine, and limit credential exposure.

Risk: The CLI can modify or remove meeting content, including a trash command with a confirmation-bypass option.

Mitigation: Require explicit user confirmation before rename, move, speaker-tagging, folder creation or changes, upload, or trash actions, and avoid `--yes` unless the user specifically approves it.

Risk: Environment-variable credentials can be exposed more broadly than intended.

Mitigation: Prefer `otter login` with OS keychain storage and scope `OTTERAI_USERNAME` and `OTTERAI_PASSWORD` only to the command session that needs them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/erickhchan/skills/otterai-cli)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may produce commands that list, retrieve, search, download, upload, rename, move, tag, or trash Otter.ai content.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
