## Description:

Mx Finance Search lets agents use natural-language queries to retrieve Eastmoney financial news, announcements, research reports, and policy updates for market monitoring and investment analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akiry09](https://clawhub.ai/user/akiry09)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent operators use this skill to query timely financial information from Eastmoney for event tracking, sentiment monitoring, announcement review, research-report summaries, and market context gathering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial search queries and the EM_API_KEY are sent to Eastmoney's service.

Mitigation: Use a revocable API key with appropriate scope and submit only queries suitable for that external service.

Risk: Returned financial search content may be written to local text files by default.

Mitigation: Use --no-save for sensitive research or manage the output directory according to local data-handling requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/akiry09/skills/mx-mx-finance-search)
- [Eastmoney Miaoxiang service](https://ai.eastmoney.com/mxClaw)

## Skill Output:

**Output Type(s):** [Text, Files, JSON]

**Output Format:** [Plain text search results, optional local .txt file, and JSON-compatible Python result fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EM_API_KEY; saves mx_finance_search_<ID>.txt by default unless --no-save is used.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
