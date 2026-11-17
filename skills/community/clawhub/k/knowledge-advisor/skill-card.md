## Description:

A Knowledge Advisor that extracts, organizes, and applies knowledge from books and learning materials to real-world situations with source-grounded citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joeyiptk](https://clawhub.ai/user/joeyiptk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ingest books or learning materials into a local knowledge base, then search, compare, and apply extracted frameworks, principles, mental models, anti-patterns, and case studies to real situations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist untrusted ingested material and later use it as the basis for advice.

Mitigation: Ingest trusted sources where possible, review extraction summaries before finalizing, and require source citations for advisory output.

Risk: The skill can fetch user-provided URLs and does not have documented URL restrictions or prompt-injection handling.

Mitigation: Avoid ingesting untrusted URLs until URL restrictions and prompt-injection handling are added; review fetched content before adding it to the knowledge base.

Risk: The skill can create, edit, and delete files under the local knowledge base and run bundled maintenance scripts.

Mitigation: Keep backups or version control for the knowledge base, review file changes before accepting them, and confirm removals before deleting book directories.

Risk: Imported book folders or metadata may be malformed because metadata validation and safe JSON/Markdown serialization are not fully documented.

Mitigation: Inspect imported folders before syncing and run the validation script after initialization, import, or rebuild operations.

## Reference(s):

- [Advisor Interaction Patterns](references/advisor-patterns.md)
- [Extraction Guide](references/extraction-guide.md)
- [Traditional Chinese Extraction Guide](references/extraction-guide-zh-hant.md)
- [Simplified Chinese Extraction Guide](references/extraction-guide-zh-hans.md)
- [Knowledge Base Schema](references/schema.md)
- [Cross-Reference Guide](references/cross-reference-guide.md)
- [Domain Detection Guide](references/domain-detection.md)
- [Health Check Reference](references/health-check.md)
- [Telegram UX Reference](references/telegram-ux.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with citations, plus Markdown and JSON knowledge-base files and shell command suggestions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports English, Traditional Chinese, and Simplified Chinese; advice is intended to cite ingested source material rather than general model knowledge.]

## Skill Version(s):

1.0.0 (source: frontmatter, release evidence, version.txt)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
