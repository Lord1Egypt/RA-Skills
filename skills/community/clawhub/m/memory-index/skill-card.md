## Description:

Memory Index provides a structured long-term memory protocol for AI agents using active and archived indexes, workspace domains, and topic files for precise context retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wzm232803119-arch](https://clawhub.ai/user/wzm232803119-arch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Memory Index to organize long-running agent work into active indexes, archived indexes, domain folders, and topic files so context can be retrieved across sessions and agent roles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unscoped memory file access or cleanup could expose, overwrite, or remove local memory data.

Mitigation: Require explicit opt-in, scoped memory roots, path validation, and backups or quarantine before cleanup.

Risk: Persisted memory files could be mistaken for higher-priority instructions during future retrieval.

Mitigation: Treat memory files as data and require current user and developer instructions to take priority before acting on retrieved content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wzm232803119-arch/skills/memory-index)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with occasional shell commands and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces memory index and topic-file structures; no executable code is included in the artifact.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
