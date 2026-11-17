## Description:

Integrate ECB Data Portal statistics through Pontx. Use for dataflows, DSDs, codelists, series keys, frequency-aware periods, bounded or incremental retrieval, availability, and SDMX formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pontjs](https://clawhub.ai/user/pontjs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to design, preview, and run bounded ECB Data Portal discovery or retrieval workflows through Pontx while preserving SDMX structure and statistical meaning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live ECB retrieval commands can make network requests or retrieve more data than intended, especially for broad wildcard queries.

Mitigation: Preview the exact bounded request, review the unchanged GET, and partition large jobs by non-overlapping keys or periods before execution.

Risk: Recurring ingestion can miss revisions or deletions if responses are treated as append-only.

Mitigation: Keep a successful checkpoint and process additions, revisions, and deletions atomically according to the live change-detection contract.

Risk: ECB observations can be misinterpreted if frequency, metadata, or revision context is omitted.

Mitigation: Preserve series metadata, report period and revision context, and avoid presenting observations as real-time, unrevised, or financial-decision-ready without authoritative support.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pontjs/skills/pontx-ecb-data-portal)
- [Pontx publisher profile](https://clawhub.ai/user/pontjs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and code-oriented instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should preview exact bounded requests before live retrieval and avoid exposing credentials or tokens.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
