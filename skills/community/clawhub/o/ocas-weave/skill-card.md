## Description: <br>
Weave maintains a private, provenance-backed social graph of people, relationships, preferences, and shared experiences for meeting prep, gift ideas, hosting, introductions, city connections, and serendipity discovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[indigokarasu](https://clawhub.ai/user/indigokarasu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use Weave to store and retrieve private social-graph facts, prepare for meetings, find gift ideas, discover connections, and sync contact data with explicit approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill retains private information about people and relationships. <br>
Mitigation: Store only durable information needed for the user's social-graph workflows and preserve provenance, timestamps, and confidence for facts. <br>
Risk: Optional Google Contacts or Clay sync can read from and write to external contact systems. <br>
Mitigation: Keep writeback disabled unless needed and require explicit approval for each sync or writeback action. <br>
Risk: The automatic daily self-update job can replace the installed skill from GitHub without per-update review. <br>
Mitigation: Disable or audit the scheduled update job and review updates manually before relying on changed behavior. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/indigokarasu/ocas-weave) <br>
- [README](README.md) <br>
- [Connectors](references/connectors.md) <br>
- [Cross-DB Linking](references/cross_db.md) <br>
- [Import & Export](references/import_export.md) <br>
- [Weave Initialization Pattern](references/init_pattern.md) <br>
- [Journal](references/journal.md) <br>
- [Query Patterns](references/query_patterns.md) <br>
- [Schemas](references/schemas.md) <br>
- [vCard Projection](references/vcard_projection.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown, JSON, Cypher snippets, and shell command proposals] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be grounded in stored facts with provenance; writeback and sync actions require explicit approval.] <br>

## Skill Version(s): <br>
2.3.0 (source: server evidence release.version and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
