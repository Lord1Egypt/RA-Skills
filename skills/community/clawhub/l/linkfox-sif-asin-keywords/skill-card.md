## Description:

Uses SIF data to reverse-lookup traffic keywords for a single Amazon ASIN, including organic and ad rankings, search volume, traffic share, conversion metrics, and week, month, or recent-day time windows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and e-commerce analysts use this skill to query keyword traffic for a specific ASIN, inspect organic and advertising rankings, and present SIF keyword metrics in readable tables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles ASIN research data, account details, phone-based onboarding, and API keys.

Mitigation: Install only if the user trusts LinkFox with this information, and prefer a safer secret store over placing API keys in shell profile files.

Risk: The skill includes paid-credit, API-key generation, and payment or order workflows.

Mitigation: Require explicit user confirmation before feedback submission, API-key generation, or any payment or order action.

Risk: The skill writes full API responses and session metadata to local LinkFox directories.

Mitigation: Review where files are written before use and avoid running the skill in a workspace that should not store ASIN research outputs.

Risk: Endpoint override environment variables can redirect API traffic away from the default LinkFox endpoints.

Mitigation: Avoid endpoint override environment variables unless the destination has been deliberately reviewed and approved.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/linkfox-ai/skills/linkfox-sif-asin-keywords)
- [SIF-ASIN keyword API reference](references/api.md)
- [Authentication and credits onboarding](references/onboarding.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance, Files]

**Output Format:** [Markdown summaries and tables with JSON responses or saved JSON file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full API responses are saved as JSON; large responses are summarized unless inline output is requested.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
