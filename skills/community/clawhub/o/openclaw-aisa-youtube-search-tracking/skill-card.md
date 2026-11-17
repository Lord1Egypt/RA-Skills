## Description:

YouTube SERP Scout for agents. Search top-ranking videos, channels, and trends for content research and competitor tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadocs](https://clawhub.ai/user/aisadocs)

### License/Terms of Use:


## Use Case:

Developers, content teams, and autonomous agents use this skill to search YouTube results for content research, competitor tracking, trend discovery, keyword research, and regional audience analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: YouTube search queries, country or language options, and filter tokens are sent to AIsa.

Mitigation: Avoid confidential or sensitive search terms and review whether sending this data to AIsa fits the deployment environment.

Risk: The skill requires an AISA_API_KEY for API access.

Mitigation: Store the API key in a protected environment variable and do not commit it to source control or share it in prompts.

Risk: The service appears to use pay-as-you-go credits.

Mitigation: Monitor usage cost and remaining credits before enabling broad or automated query workloads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aisadocs/skills/openclaw-aisa-youtube-search-tracking)
- [OpenClaw homepage](https://openclaw.ai)
- [AIsa API reference](https://aisa.mintlify.app/api-reference/introduction)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash, Python, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses AISA_API_KEY and returns YouTube search result data from the AIsa API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
