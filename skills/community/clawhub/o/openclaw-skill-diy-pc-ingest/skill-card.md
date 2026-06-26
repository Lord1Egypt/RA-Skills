## Description: <br>
Ingests pasted PC parts purchase and configuration text into Notion DIY_PC tables, helping agents classify items, enrich details, ask clarifying questions, and upsert rows through the Notion data_sources API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NEXTAltair](https://clawhub.ai/user/NEXTAltair) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, PC builders, and workspace maintainers use this skill to turn raw PC parts receipts, Discord notes, and configuration snippets into reviewed Notion records for DIY_PC inventory tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write, overwrite, or archive Notion pages when configured with a Notion integration token. <br>
Mitigation: Use a Notion integration shared only with the intended DIY_PC databases, review generated JSONL before running it, and avoid page_id, overwrite, archive, or mirror_to_pcconfig unless explicitly requested. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/NEXTAltair/openclaw-skill-diy-pc-ingest) <br>
- [Notion Skill Dependency](https://clawhub.ai/steipete/notion) <br>
- [Configuration Example](references/config.example.json) <br>
- [Notion ID Setup Notes](references/notion-ids.md) <br>
- [Notion Integration Setup](https://www.notion.so/my-integrations) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSONL records and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Notion API credentials and local target IDs; review generated JSONL before applying changes.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
