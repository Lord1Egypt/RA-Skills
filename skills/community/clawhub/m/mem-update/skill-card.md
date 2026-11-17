## Description:

Mem Update Publish guides an agent through a v6.12 memory-bank update workflow for project-aware markdown task, session, implementation, and edit-history records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[space-cadet](https://clawhub.ai/user/space-cadet)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when updating a memory-bank repository after project work. It helps maintain task files, task registries, implementation notes, session records, session cache, canonical edit chunks, and generated edit history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow modifies persistent memory-bank markdown records, so an incorrect project or task selection can put history in the wrong location.

Mitigation: Confirm the active project and memory-bank location before editing; the artifact's Step 0 requires checking project repositories before workspace-level memory-bank files.

Risk: Documentation updates can become inaccurate when the agent lacks a complete record of prior work.

Mitigation: Use the discovery steps to inspect edit history, session cache, git history, uncommitted changes, and existing edit chunks before updating records.

Risk: Manual edits to the generated edit_history.md view can corrupt the canonical history.

Mitigation: Create canonical edit chunk files under memory-bank/edits and regenerate edit_history.md instead of editing the generated view directly.

## Reference(s):

- [Memory Bank integrated rules v6.12](${MB_CORE_PATH}/integrated-rules-v6.12.md)
- [Memory Bank templates](${MB_CORE_PATH}/memory-bank/templates/)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces instructions for updating existing memory-bank markdown files and creating canonical edit chunk markdown; does not produce database records.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
