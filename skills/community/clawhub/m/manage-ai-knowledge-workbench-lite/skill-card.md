## Description:

AI Knowledge Workbench Lite builds and refreshes a local, metadata-only Markdown or Obsidian knowledge index and offline dashboard in one authorized workspace while keeping source notes read-only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexfengrui](https://clawhub.ai/user/alexfengrui)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers, knowledge workers, and agent users use this skill to initialize, inspect, update, and safely uninstall a local metadata-only knowledge workbench for an authorized Markdown folder or Obsidian vault. It is suited for local indexing and dashboard generation where source notes should remain the fact source and derived outputs should stay separate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable workspace configuration can redirect later scans to other readable local folders.

Mitigation: Protect .ai-workbench/workbench.json and recheck configured source roots before scan or update operations, especially in shared or writable workspaces.

Risk: The local parser scans and stores metadata about files under configured source roots.

Mitigation: Use only explicitly authorized source directories and keep sensitive or unknown records out of visible dashboard views.

Risk: The dashboard verification step briefly binds a local loopback service.

Mitigation: Limit verification to ephemeral 127.0.0.1 use and do not treat the skill as a persistent web service.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alexfengrui/skills/manage-ai-knowledge-workbench-lite)
- [Privacy Boundary](references/PRIVACY.md)
- [Runtime Contract](references/RUNTIME_CONTRACT.md)
- [Autonomy Gates](references/AUTONOMY_GATES.md)
- [Python Downloads](https://www.python.org/downloads/)
- [Obsidian Download](https://obsidian.md/download)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON command results plus generated Markdown indexes and offline HTML dashboard files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes derived outputs under .ai-workbench, AI-Knowledge, and AI-Dashboard inside the selected workspace; source notes remain read-only.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
