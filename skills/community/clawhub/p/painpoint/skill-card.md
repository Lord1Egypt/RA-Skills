## Description:

Summarizes the latest NicheStarter weekly pain-point report from the public preview API, lists the top five pain points, and guides users to sign in for the full report and free weekly email subscription.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shujip](https://clawhub.ai/user/shujip)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch NicheStarter's public weekly pain-point preview, produce a short digest of the top five current pain points, and include sign-in and free weekly email calls to action. It can also support scheduled weekly delivery through an agent or scheduler.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic email, Slack, or DM delivery could send previews or links to unintended recipients.

Mitigation: Review scheduler recipients before enabling automated delivery.

Risk: CTA and source links are taken from the public API response and may need review before redistribution.

Mitigation: Review generated links before automatic delivery, especially in external channels.

Risk: A scheduled job could send the same weekly report more than once.

Mitigation: Persist the last sent report.id and skip delivery when the API returns the same report again.

Risk: Unavailable or empty API responses could lead to invented or stale content.

Mitigation: Use the documented fallback for 404 or empty results and do not fabricate pain points, rankings, or subscriber counts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shujip/skills/painpoint)
- [Publisher profile](https://clawhub.ai/user/shujip)
- [Weekly report preview API](https://www.nichestarter.ai/api/public/weekly-report-preview)
- [NicheStarter](https://www.nichestarter.ai)
- [API reference](reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown digest with optional plain-text links and scheduler setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public API response data only; scheduled delivery should deduplicate by report.id.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
