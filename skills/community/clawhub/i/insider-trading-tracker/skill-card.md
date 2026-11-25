## Description:

Retrieves SEC Form 4 insider activity by ticker and market, including cluster buys and 10b5-1 plan indicators, through the read-only SentiSense API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thesentitrader](https://clawhub.ai/user/thesentitrader)

### License/Terms of Use:

MIT-0

## Use Case:

Investors and analysts use the skill to inspect disclosed insider transactions, market-wide activity, and cluster buys as informational context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scan was partial with medium confidence because some local path-like references could not be resolved.

Mitigation: Review the skill instructions and any referenced material available before installation.

Risk: A free-tier preview may contain only the newest five filings, which cannot establish full-window totals or absence of insider buying.

Mitigation: Check preview status and totalCount, and qualify conclusions when the response is truncated.

Risk: Awards, exercises, gifts, plan purchases, and tax withholding can be mistaken for discretionary insider buying or selling.

Mitigation: Separate open-market P/S trades from corporate mechanics, exclude plan purchases from buy counts, and identify confirmed 10b5-1 sales.

## Reference(s):

- [SentiSense API documentation](https://sentisense.ai/docs/api/#full-sample-responses-with-a-free-key)
- [SentiSense](https://sentisense.ai)
- [ClawHub skill release](https://clawhub.ai/thesentitrader/skills/insider-trading-tracker)

## Skill Output:

**Output Type(s):** [Analysis, Text, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Informational summaries based on returned API data; free-tier responses may be previews.]

## Skill Version(s):

1.2.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
