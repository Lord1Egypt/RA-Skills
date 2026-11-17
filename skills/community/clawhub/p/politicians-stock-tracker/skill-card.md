## Description:

Summarizes U.S. congressional stock-trade disclosures by member or ticker through the read-only SentiSense API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thesentitrader](https://clawhub.ai/user/thesentitrader)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and other users can review U.S. congressional trade disclosures, compare activity by politician or ticker, and understand filing delays without placing trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries go to SentiSense and may use a SentiSense API key.

Mitigation: Review external data sharing before querying, and keep the API key out of prompts and outputs.

Risk: Delayed disclosures and limited preview results can mislead financial decisions.

Mitigation: Label transaction and disclosure dates, amount ranges, and incomplete previews; present results as information, not investment advice.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/thesentitrader/skills/politicians-stock-tracker)
- [SentiSense](https://sentisense.ai)
- [SentiSense API key](https://app.sentisense.ai/get-api-key)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown summaries of congressional trading disclosures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports amount ranges and transaction and disclosure dates; labels partial previews.]

## Skill Version(s):

1.1.7 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
