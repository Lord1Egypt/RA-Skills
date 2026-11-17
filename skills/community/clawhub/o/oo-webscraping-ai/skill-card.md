## Description:

WebScraping.AI (webscraping.ai). Use this skill for ANY WebScraping.AI request — searching and reading data. Whenever a task involves WebScraping.AI, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agents use the skill to search and read web data through a connected WebScraping.AI account. It provides actions for extracting page text, fetching rendered HTML, selecting page areas, and checking account information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup can execute an unverified remote installer without a separate user approval step.

Mitigation: Review and approve CLI installation separately, preferably using a verified fixed release; check whether bundled-skill synchronization is acceptable before first use.

Risk: Requests use the connected OOMOL/WebScraping.AI account and may consume credits.

Mitigation: Check account and credit usage before running actions when consumption matters.

## Reference(s):

- [WebScraping.AI API documentation](https://webscraping.ai/docs)
- [WebScraping.AI](https://webscraping.ai)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Text, HTML, JSON, Shell commands, Guidance]

**Output Format:** [JSON action responses with extracted text, HTML, or account information; Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Response content depends on the selected action and target page.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
