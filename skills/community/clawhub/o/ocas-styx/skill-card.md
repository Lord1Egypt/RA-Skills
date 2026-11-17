## Description:

Styx provides a transaction data store with merchant enrichment, exposing clean, queryable bank transaction data and resolved merchant records for downstream spending and consumption analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[indigokarasu](https://clawhub.ai/user/indigokarasu)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use Styx to sync Plaid transaction data, enrich obfuscated merchant names, query spending and merchant history, and supply clean transaction signals to downstream skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles banking records, Plaid tokens, Google/Places keys, and possible Gmail receipt content.

Mitigation: Grant only the minimum required local database and secret access, confirm user consent and retention expectations, and clarify Gmail receipt scope before enabling ingestion or enrichment.

Risk: Sync and enrichment workflows can change local financial databases and may run from scheduled cron jobs.

Mitigation: Default to read-only query usage until write or sync mode is explicitly approved, back up relevant databases, and review scheduled commands before deployment.

Risk: Self-update instructions and version drift can introduce unreviewed code into a sensitive financial workflow.

Mitigation: Pin a reviewed release, remove or gate self-update steps, and rescan the artifact before upgrading.

## Reference(s):

- [Data Flow](references/data-flow.md)
- [Query API](references/query-api.md)
- [Schema](references/schema.md)
- [Financial Sync](references/financial-sync.md)
- [Enrichment Pipeline](references/enrichment-pipeline.md)
- [Styx Data Provenance](references/provenance.md)
- [Receipt Parsing](references/receipt-parsing.md)
- [Cron Gotchas](references/cron-gotchas.md)
- [Self Update](references/self_update.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell, SQL, and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local database paths, sync modes, cron workflows, and review queues that require operator confirmation before execution.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
