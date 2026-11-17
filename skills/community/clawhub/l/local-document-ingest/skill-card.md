## Description:

Ingests desktop-uploaded local files into a Research KB by validating input files, extracting readable content, guiding entity-page creation, archiving sources, updating catalog and index metadata, and returning backend task JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myd2002](https://clawhub.ai/user/myd2002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to turn uploaded local-folder changes into traceable Research KB wiki pages. It is intended for backend-controlled ingestion flows where every readable input file receives an entity page, related pages can be updated, and source files are archived for provenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payload-supplied file paths and result paths could expose local files or overwrite writable files if accepted without controls.

Mitigation: Run only in a controlled backend that resolves symlinks and restricts storagePath and resultFile to approved directories.

Risk: Payload-supplied Gitea settings and broad bot credentials could redirect writes or leak the bot token.

Mitigation: Use fixed allowlisted Gitea origins and a narrowly scoped bot token under a low-privilege account.

Risk: Unpinned Python dependencies can change behavior or introduce supply-chain risk.

Mitigation: Pin dependencies with hashes before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/myd2002/skills/local-document-ingest)
- [Publisher Profile](https://clawhub.ai/user/myd2002)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown knowledge pages, JSON task envelopes, and shell command workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Archives source files under source_files/local_folder, writes or updates catalog/index metadata, and returns result JSON with a boolean success field.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
