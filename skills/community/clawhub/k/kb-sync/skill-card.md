## Description:

kb-sync helps agents preview incremental differences between local Markdown/text notes and a manifest before users approve knowledge-base synchronization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge-base maintainers use this skill to review adds, updates, and deletes in a local notes directory before deciding what to sync to IMA, Tencent LeXiang, or a generic API. It is most appropriate when users need a dry-run change list and manual confirmation before any write operation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can scan broad local directories and includes .json and text files that may contain secrets or personal data.

Mitigation: Run it only against a narrow notes-only directory, avoid JSON/text files that may contain credentials, and inspect the dry-run file list before any sync.

Risk: The release claims cloud knowledge-base sync while the artifact primarily ships a local diff scanner and guidance for external connectors.

Mitigation: Treat cloud sync steps as manual integration guidance, confirm the exact destination and connector behavior, and do not allow API upserts until the target files are reviewed.

Risk: The learner script can persist local usage notes, errors, and preferences in learned_patterns.json.

Mitigation: Do not record sensitive notes, tokens, or private destinations in learner entries, and review or delete learned_patterns.json when appropriate.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and local diff summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run diff output by default; manifest updates occur only when explicitly run without dry-run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
