## Description:

Research Google Maps and Shopping reviews for any company. Run multi-brand monitoring with heartbeat refreshes and sentiment reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users, reputation teams, and analysts use this skill to research Google Maps and Shopping review signals for a company, compare competitors, and optionally set up recurring monitoring with heartbeat refreshes, sentiment trends, and reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Monitoring mode can create local state under ~/google-reviews/ containing brand watchlists, snapshots, reports, cadence, and alert preferences.

Mitigation: Confirm before the first write, use stay-quiet activation when only explicit invocation is desired, and avoid storing credentials or private customer identifiers in memory files.

Risk: Google API or user-approved page access sends brand identifiers and review query parameters to Google endpoints.

Mitigation: Use authorized or user-approved access methods, keep connector permissions explicit, and report degraded or blocked sources instead of claiming live results.

Risk: Review sentiment and trend conclusions can be misleading when source coverage is sparse or the review window is small.

Mitigation: Pair sentiment with source evidence, state confidence, and preserve source-native identifiers and timestamps for traceability.

## Reference(s):

- [Google Reviews ClawHub listing](https://clawhub.ai/ivangdavila/skills/google-reviews)
- [Google Reviews homepage](https://clawic.com/skills/google-reviews)
- [Google Business Profile API endpoint](https://mybusiness.googleapis.com)
- [Google Merchant API endpoint](https://merchantapi.googleapis.com)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional shell commands and JSON/JSONL review snapshots]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local monitoring state under ~/google-reviews/ when monitoring is enabled.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
