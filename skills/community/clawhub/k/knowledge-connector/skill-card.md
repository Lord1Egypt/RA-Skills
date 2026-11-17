## Description:

Knowledge Connector helps agents import local notes and documents, run cross-document search, build relationship maps, and produce concrete next actions while preserving a clear privacy boundary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, knowledge workers, and agents use this skill to verify a local knowledge store, import notes or document folders, search across sources, inspect concept maps, and decide what to connect or review next.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Imported notes can contain sensitive content, and the local store keeps document-derived excerpts and paths.

Mitigation: Review notes before import, avoid uploading sensitive material to external tools unless explicitly chosen, and place KC_DATA_DIR in a protected local directory.

Risk: HTML visualization exports load live third-party code while embedding data derived from local notes.

Mitigation: Treat exported HTML graphs as not fully offline unless the remote visualization dependency is bundled or pinned before sharing or opening in sensitive environments.

Risk: Export, import, and clear commands mutate the local knowledge store.

Mitigation: Use those commands deliberately, keep backups for important stores, and review command targets before running destructive or bulk operations.

## Reference(s):

- [Knowledge Connector ClawHub skill page](https://clawhub.ai/harrylabsj/skills/knowledge-connector)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON, HTML, or DOT file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local knowledge-store files and exported graph or backup files when the user runs the corresponding commands.]

## Skill Version(s):

1.4.0 (source: server release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
