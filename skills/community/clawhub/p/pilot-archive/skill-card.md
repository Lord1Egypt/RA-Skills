## Description:

Index and search historical data exchanges, messages, and file transfers over Pilot Protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

AGPL-3.0

## Use Case:

Developers and operators use this skill to index Pilot Protocol inbox messages and received file-transfer records into local searchable archives for history review, audit, and communication-pattern analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can copy Pilot message bodies, sender metadata, filenames, ports, and transfer details into local plaintext archive files with open-ended retention.

Mitigation: Set restrictive permissions on archive directories and files, avoid archiving secrets, and delete or rotate archives when long-term retention is unnecessary.

Risk: The archive workflow is unclear about using current inbox data while presenting the result as historical archive data.

Mitigation: Confirm the intended data source and retention scope before indexing, and review generated shell commands before execution.

## Reference(s):

- [Pilot Protocol Homepage](https://pilotprotocol.network)
- [Pilot Archive on ClawHub](https://clawhub.ai/teoslayer/skills/pilot-archive)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local plaintext JSONL archive examples that depend on pilotctl, jq, and a running Pilot daemon.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
