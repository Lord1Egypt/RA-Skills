## Description: <br>
Persistent, incremental, searchable persona knowledge base. Ingests data from Obsidian vaults, chat exports, X/Twitter archives, and more into a MemPalace-backed store with a Karpathy LLM Wiki knowledge layer. Exports training/ directories for persona-model-trainer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neiljo-gy](https://clawhub.ai/user/neiljo-gy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to initialize, ingest, search, maintain, and export a persistent persona knowledge base from local notes, chat exports, social archives, and related source files. It is intended for persona dataset preparation and downstream persona-model training workflows, not quick one-shot summarization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create long-lived local persona datasets from private notes, messages, social archives, and chat databases. <br>
Mitigation: Use it only for intentional persona dataset creation, confirm the dataset slug and subject, and avoid broad personal directories or chat.db unless that source is explicitly needed. <br>
Risk: Social and chat archive ingestion can include direct messages, third-party messages, phone numbers, emails, passwords, and other sensitive content. <br>
Mitigation: Run dry runs carefully, remove DM and unrelated folders before ingestion, review PII flags, and manually redact sensitive source material before retaining or exporting it. <br>
Risk: Training exports may copy raw source files and preserve sensitive material. <br>
Mitigation: Treat training directories as sensitive data, restrict sharing and storage, and use wiki-only export mode when raw source copying is not required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/neiljo-gy/persona-knowledge) <br>
- [Source formats](artifact/references/source-formats.md) <br>
- [Wiki schema](artifact/references/wiki-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSONL datasets, Markdown wiki pages, and training export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist local knowledge stores, source backups, wiki pages, and training exports under the configured OpenPersona knowledge path.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
