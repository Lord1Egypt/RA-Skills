## Description: <br>
Build and maintain a local Markdown knowledge wiki that compounds over time instead of relying on one-shot RAG retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lhuaizhong](https://clawhub.ai/user/lhuaizhong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, teams, and knowledge workers use this skill to turn notes, documents, transcripts, chat logs, and project context into a local Markdown wiki. It helps agents ingest sources, answer questions from compiled pages, reindex the vault, lint stale or unsupported claims, and initialize an Obsidian-friendly scaffold. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and update notes, documents, transcripts, chat logs, and wiki files placed in the vault. <br>
Mitigation: Use a dedicated knowledge directory, review large ingests, preserve raw sources, and inspect generated or modified Markdown before relying on it. <br>
Risk: Starter scaffold files can be replaced when the initializer is run with --force. <br>
Mitigation: Use --force only when intentionally refreshing scaffold files, and keep backups or version control for important vault content. <br>
Risk: Compiled wiki pages may contain stale, unsupported, or conflicting summaries as source material changes. <br>
Mitigation: Run the lint and reindex workflows, keep source pointers on high-value claims, and preserve disagreement explicitly when evidence is mixed. <br>


## Reference(s): <br>
- [Operations](references/operations.md) <br>
- [Scaffold](references/scaffold.md) <br>
- [Publish Notes](references/publish-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with optional shell commands and generated Markdown scaffold files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled initializer creates local wiki directories and starter Markdown files; --force intentionally replaces existing scaffold files.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
