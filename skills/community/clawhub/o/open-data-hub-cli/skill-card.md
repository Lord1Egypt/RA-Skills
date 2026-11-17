## Description:

Query Open Data Hub/NOI Techpark data through `odh`: Tourism, Mobility, traffic, A22, parking, EV charging, STA GTFS, and transit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galjos](https://clawhub.ai/user/galjos)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to guide agents in querying Open Data Hub and NOI Techpark datasets through the `odh` CLI instead of scraping pages or guessing API calls. It supports public transport, tourism, mobility, traffic, parking, EV charging, A22, and STA GTFS workflows while preserving source, freshness, truncation, and warning context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on installing and executing the external `odh` CLI, which may make network requests to Open Data Hub services.

Mitigation: Confirm the pinned Go module or Homebrew tap is acceptable before installation, and run the CLI in an environment approved for outbound requests.

Risk: Answers based on live public feeds can be stale, truncated, incomplete, or tied to source-specific caveats.

Mitigation: Surface freshness, truncation, coverage, source, provenance, and warning fields in user-facing answers, as the skill instructs.

## Reference(s):

- [Open Data Hub API](https://opendatahub.com/api/)
- [Open Data Hub datasets documentation](https://docs.opendatahub.com/en/latest/datasets.html)
- [Open Data Hub Mobility API getting started](https://docs.opendatahub.com/en/latest/howto/mobility/getstarted.html)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text, markdown]

**Output Format:** [Markdown guidance with inline shell commands and expected JSON/table output notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance emphasizes read-oriented data queries, explicit JSON parsing flags, source fields, warnings, freshness, and truncation checks.]

## Skill Version(s):

0.7.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
