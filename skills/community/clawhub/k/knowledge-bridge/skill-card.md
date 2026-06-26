## Description: <br>
Knowledge Bridge ingests insights from a local insight engine into a SQLite and LlamaIndex knowledge base, then supports categorization, deduplication, search, statistics, backfill, and explanation commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge-work agents use this skill to keep a local knowledge base synchronized with insight-engine outputs and to query, summarize, or explain stored knowledge entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ingest and backfill can import and retain local insight-engine records in the configured knowledge base. <br>
Mitigation: Confirm the local module and SQLite database path belong to the intended workspace, and run ingest or backfill only for data you are comfortable storing. <br>
Risk: Historical backfill can import more records than a single latest-cycle ingest. <br>
Mitigation: Inspect stored entries after backfill and maintain a deletion or cleanup process for records that should not remain in the knowledge base. <br>


## Reference(s): <br>
- [Knowledge Bridge on ClawHub](https://clawhub.ai/534422530/knowledge-bridge) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [JSON-compatible dictionaries and plain text messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports ingest, search, stats, backfill, and explain command modes; backfill may process historical records.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
