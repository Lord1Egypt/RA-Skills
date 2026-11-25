## Description:

Integrates Lucernel's public daily World English Bible verse endpoint. Use when a task needs today's verse or a verse for a specified calendar date.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucernel](https://clawhub.ai/user/lucernel)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to retrieve the World English Bible verse selected for the current UTC date or a valid specified date, then present its reference and source attribution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is partial because a referenced path was missing, leaving the related API guidance unresolved.

Mitigation: Review the complete API error and rate-limit guidance before installation, and honor Retry-After with bounded retries for HTTP 429 or 503 responses.

## Reference(s):

- [Daily verse API endpoint](https://lucernel.com/api/public/v1/daily-verse)
- [Daily Bible verse source page](https://lucernel.com/tools/daily-bible-verse)

## Skill Output:

**Output Type(s):** [API Calls, Text, Guidance]

**Output Format:** [Verse text with date, reference, translation, and source attribution; optionally presented as Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the current UTC date by default or a specified date from 1900 through 2100; preserves the response fields and World English Bible attribution.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
