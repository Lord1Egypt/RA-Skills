## Description:

Parses a loan-outreach recording request, clarifies the time range and analysis focus, fetches ASR transcript records, and guides generation of a transcript-grounded outreach insight report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[legionspace-hackathon](https://clawhub.ai/user/legionspace-hackathon)

### License/Terms of Use:

MIT-0

## Use Case:

External business and operations users use this skill to request ASR transcript analysis for loan outreach recordings. The skill clarifies ambiguous time windows or analysis dimensions before transcript retrieval and supports default ten-dimension outreach reporting or a user-selected focus.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bearer tokens, tenant identifiers, and transcript records are handled with too little scoping or protection.

Mitigation: Add endpoint allowlisting, HTTPS, tenant binding, transcript and field minimization, and bounded redacted error logging before installation.

Risk: Use with real customer or employee recordings could expose sensitive transcript data before required controls are in place.

Mitigation: Do not use real customer or employee recordings until the controls listed in the security guidance have been implemented and reviewed.

Risk: The packaged scripts are reported to contain a JavaScript syntax error in parse-time-range.mjs, so the skill does not run as packaged.

Mitigation: Fix and validate parse-time-range.mjs before relying on the skill in any workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/legionspace-hackathon/skills/legion-loan-outreach-insight)
- [Publisher profile](https://clawhub.ai/user/legionspace-hackathon)
- [Insight report template](templates/insight-report-page.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [JSON from helper scripts and Markdown or plain-text report content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports should be grounded only in ASR transcript text and may include clarification questions before data retrieval.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
