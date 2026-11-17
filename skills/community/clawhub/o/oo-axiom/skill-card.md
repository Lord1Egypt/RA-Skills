## Description:

Axiom (axiom.co). Use this skill for ANY Axiom request — reading, creating, updating, and deleting data. Whenever a task involves Axiom, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query Axiom and inspect, create, or delete datasets through an OOMOL-connected account. It guides users to inspect action schemas first and requires confirmation for changes that write or delete data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup uses online installers that are unpinned, and the downloaded binary was not verified.

Mitigation: Review and approve CLI installation separately, and verify the installer and binary before running them.

Risk: CLI startup synchronization can install skills across agent hosts, and the scope of those changes is under-described.

Mitigation: Review skill changes and disable startup synchronization with OO_SKILLS_SYNC_DISABLED as documented in the command reference when appropriate.

Risk: Dataset creation and deletion change or remove Axiom data.

Mitigation: Keep explicit approval for dataset creation and deletion, confirming the exact target and operation before execution.

## Reference(s):

- [Axiom REST API documentation](https://axiom.co/docs/restapi/introduction)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance, Text]

**Output Format:** [Markdown guidance, JSON action payloads, and Axiom query or dataset responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write and destructive dataset operations require explicit confirmation.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
