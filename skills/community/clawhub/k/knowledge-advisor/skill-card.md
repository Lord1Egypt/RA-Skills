## Description: <br>
Knowledge Advisor extracts, organizes, searches, and applies knowledge from user-ingested books and learning materials while requiring citations to the source material. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joeyiptk](https://clawhub.ai/user/joeyiptk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to build and manage a local book-based knowledge base, then ask grounded questions that are answered from ingested materials with source citations. It supports ingestion, search, advisory responses, domain listing, health checks, sync, and removal workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Finalized ingestions and sync operations write or rewrite local knowledge-base files. <br>
Mitigation: Review ingestion summaries before finalizing and keep backups or version control for important knowledge-base directories. <br>
Risk: Remove workflows can delete a selected book directory after confirmation. <br>
Mitigation: Confirm the selected book carefully before removal and recover from backup if deleted content must be restored. <br>
Risk: Private documents or sensitive URLs may be stored locally as extracted content or source metadata. <br>
Mitigation: Avoid ingesting confidential documents or URLs containing tokens unless local storage of that information is acceptable. <br>


## Reference(s): <br>
- [Extraction Guide](references/extraction-guide.md) <br>
- [Advisor Patterns](references/advisor-patterns.md) <br>
- [Knowledge Base Schema](references/schema.md) <br>
- [Cross-Reference Guide](references/cross-reference-guide.md) <br>
- [Health Check](references/health-check.md) <br>
- [Domain Detection](references/domain-detection.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/joeyiptk/knowledge-advisor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with cited guidance, generated knowledge-base files, JSON metadata, and shell command output for maintenance workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advice is expected to be grounded in the user's local knowledge base and to cite book, chapter or section, and framework when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, version.txt, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
