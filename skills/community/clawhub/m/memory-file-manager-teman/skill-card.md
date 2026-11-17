## Description:

A proactive memory distillation skill that maintains MEMORY.md through scheduled or user-triggered review, memory organization, recall inspection, and Obsidian indexing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teman2050](https://clawhub.ai/user/teman2050)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use Dream to keep long-term memory concise, searchable, and archived by distilling daily memory journals into MEMORY.md, a permanent ledger, and optional Obsidian indexes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is a high-retention memory system: archived memories are kept indefinitely, forget operations do not purge the archive, and forgotten topics can re-enter active memory.

Mitigation: Review retention expectations before installation, keep sensitive data out of memory entries, and add an explicit archive-purge process if permanent retention is not acceptable.

Risk: Scheduled and some memory updates can run silently, which may change local memory files without immediate user review.

Mitigation: Enable review of monthly logs and MEMORY.md changes, and require manual triggering where silent scheduled updates are not acceptable.

Risk: The security review reports local file-safety flaws in script behavior, including path scoping for --atomic-write and parsing of last-review.txt.

Mitigation: Fix and re-review the script before use, especially path validation and timestamp parsing, and run it only in a constrained workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/teman2050/skills/memory-file-manager-teman)
- [Project homepage](https://github.com/teman2050/dream-skill)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command invocations and local Markdown, JSON, and text file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains MEMORY.md, an append-only ledger, metadata files, and Obsidian index files under configured local paths.]

## Skill Version(s):

0.2.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
