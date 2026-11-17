## Description:

Analyzes annual patent filing trends for a technology, compares leading applicants over time, identifies new entrants, and produces an Excel-compatible trend table.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts and R&D teams use the skill to assess how patent activity in a technology area changes over time, compare applicant activity across periods, and identify new entrants for reports and planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Patent queries go to PatentMax and may incur disclosed charges.

Mitigation: Use nonconfidential search terms and review the disclosed costs before running queries.

Risk: Paid API-key handling needs review before use.

Mitigation: Before supplying a paid key, require HTTPS-only authenticated requests, safe redirect handling, and private credential storage; do not send keys through chat.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/ip930/skills/patent-trend-analysis)
- [PatentMax](https://ip930.com)
- [PatentMax API](https://api.ip930.com)

## Skill Output:

**Output Type(s):** [Analysis, CSV file, Text]

**Output Format:** [CSV trend table with a written summary and new-entrant list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The trend table is Excel-compatible.]

## Skill Version(s):

1.0.2 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
