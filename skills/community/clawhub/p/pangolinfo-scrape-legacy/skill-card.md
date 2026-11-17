## Description:

Search Google and scrape Amazon using Pangolin APIs, including AI Mode search, SERP results with AI Overview extraction, Amazon product and listing scraping, and screenshot capture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tammy-hash](https://clawhub.ai/user/tammy-hash)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run Pangolin-backed Google search, Google AI Overview, multi-turn AI Mode, and Amazon scraping workflows from a local Python client. It is useful for collecting structured search results, AI overview content with references, screenshots, and Amazon product or listing data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports that the skill stores a long-lived Pangolin access token in a predictable local file.

Mitigation: Prefer PANGOLIN_TOKEN where possible, protect or remove ~/.pangolin_token after use, and treat the token as account access.

Risk: Searches, Amazon URLs, screenshot requests, follow-up prompts, and Pangolin credentials or tokens are sent to Pangolin.

Mitigation: Install and run the skill only when this data sharing is acceptable, and avoid submitting sensitive prompts, URLs, or credentials outside the documented authentication variables.

## Reference(s):

- [Pangolinfo Scrape (Legacy) ClawHub Page](https://clawhub.ai/tammy-hash/skills/pangolinfo-scrape-legacy)
- [Pangolinfo AI SERP Canonical Skill](https://clawhub.ai/pangolinfo/pangolinfo-ai-serp)
- [Pangolinfo Amazon Scraper Canonical Skill](https://clawhub.ai/pangolinfo/pangolinfo-amazon-scraper)
- [Pangolin Website](https://www.pangolinfo.com)
- [AI Mode API Reference](references/ai-mode-api.md)
- [AI Overview SERP API Reference](references/ai-overview-serp-api.md)
- [Amazon Scrape API Reference](references/amazon-api.md)
- [Error Codes and Troubleshooting](references/error-codes.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with bash examples and structured JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include task IDs, AI overview text and references, organic search results, screenshot URLs, Amazon product records, errors, and authentication status.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact _meta.json reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
