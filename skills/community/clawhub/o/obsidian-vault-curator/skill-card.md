## Description:

Cautious curation, classification, review, and migration planning for Obsidian or Markdown vaults.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thenerdforge](https://clawhub.ai/user/thenerdforge)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to organize Obsidian or Markdown vaults, classify notes, preserve historical context, design review views, and plan small, reviewable migrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Vault notes may contain secrets, PII, operational details, or internal-only identifiers.

Mitigation: Review proposed write slices before allowing edits, and verify sensitive-content hypotheses against exact note text before escalation or changes.

Risk: Large restructures, deletes, or rewrites can lose historical context or break links.

Mitigation: Inventory first, keep write slices small, avoid deletes unless explicitly requested, and verify frontmatter and links after each write slice.

Risk: Classification or canonical-page recommendations can be wrong when evidence is incomplete or notes conflict.

Mitigation: Treat subagent findings as candidates, prefer needs-review under uncertainty, and use human-review gates for contested or high-impact changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thenerdforge/skills/obsidian-vault-curator)
- [bases-views.md](references/bases-views.md)
- [classification-rubric.md](references/classification-rubric.md)
- [output-format.md](references/output-format.md)
- [status-schema.md](references/status-schema.md)
- [subagent-packets.md](references/subagent-packets.md)
- [subagents.md](references/subagents.md)
- [workflow.md](references/workflow.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional JSON, YAML frontmatter, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses compact five-section summaries for curation findings and merge reports.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
