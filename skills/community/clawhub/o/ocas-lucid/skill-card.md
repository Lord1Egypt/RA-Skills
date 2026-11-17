## Description:

Nightly journal curator that batch-processes OCAS skill journals, classifies them for relevance, and writes curated journal content for a configured memory provider to ingest.

This skill is ready for commercial/non-commercial use.

## Publisher:

[indigokarasu](https://clawhub.ai/user/indigokarasu)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use Lucid to run scheduled or manual journal curation across OCAS skills, classify journal entries, and preserve relevant content for memory ingestion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaged skill includes scheduled persistence and a silent Git self-update path that can overwrite local skill changes.

Mitigation: Disable or remove the daily update job unless the publisher source is explicitly trusted; prefer manual, reviewed updates pinned to commits or signed releases.

Risk: Journal curation can write selected journal content and structured records to the configured memory provider.

Mitigation: Review the storage and memory-provider configuration before first use, and run a manual status or dry operational review before enabling scheduled execution.

## Reference(s):

- [Classification Reference](references/classification.md)
- [Cron Execution - Lucid Dream Cycle](references/cron-execution.md)
- [Dream Cycle](references/dream-cycle.md)
- [Dream Journal](references/dream-journal.md)
- [Safety Gates](references/safety-gates.md)
- [Lucid - Self-Update Procedure](references/self-update-lucid.md)
- [Lucid - OKR Evaluation](references/okr.md)
- [Gotchas - Lucid Dream Cycle](references/gotchas.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, code references, and JSON/file schemas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local journal and data files during execution; may write to a configured memory provider.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; packaged skill metadata version 3.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
