## Description:

Multi search engine integration with 16 engines (7 CN + 9 Global). Supports advanced search operators, time filters, site search, privacy engines, and WolframAlpha knowledge queries. No API keys required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[handy01](https://clawhub.ai/user/handy01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and agents use this skill to route search queries across Chinese and global search engines, apply advanced search operators and filters, and aggregate successful results into a concise search report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries may be transmitted to selected third-party search engines, potentially multiple providers per request, despite the artifact's privacy notice stating there is no external data transmission.

Mitigation: Do not use the skill for passwords, API keys, private source code, internal URLs, regulated data, or confidential business searches unless provider selection is explicit and the privacy notice is corrected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/handy01/skills/handy01-multi-search-engine)
- [Domestic search guide](references/advanced-search.md)
- [International search guide](references/international-search.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Markdown search report with inline web_fetch request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search queries may be sent to multiple third-party search engines before successful results are aggregated.]

## Skill Version(s):

2.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
