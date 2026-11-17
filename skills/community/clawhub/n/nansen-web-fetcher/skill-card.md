## Description:

Fetch and analyze content from one or more URLs using AI (Gemini 2.5 Flash). Use when you have specific URLs and need to extract or summarize their content. Pairs well with `nansen web search` results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to retrieve content from specified URLs and get an AI-generated answer or summary tailored to a question.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted URLs or questions may contain credentials or confidential information sent for external processing.

Mitigation: Review URLs and questions before submitting them, and remove credentials and confidential details.

## Reference(s):

- [Nansen Web Fetcher on ClawHub](https://clawhub.ai/nansen-devops/skills/nansen-web-fetcher)
- [Browser Login Platform Scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)

## Skill Output:

**Output Type(s):** [Analysis, JSON]

**Output Format:** [JSON with an AI-generated analysis and retrieved and failed URL lists; optionally pretty-printed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts up to 20 URLs per request; requests have a 30-second timeout.]

## Skill Version(s):

0.1.3 (source: server-resolved ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
