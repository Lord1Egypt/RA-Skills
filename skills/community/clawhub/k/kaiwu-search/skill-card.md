## Description:

Search the web in Chinese (Traditional + Simplified) and English using the Kaiwu API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daaab](https://clawhub.ai/user/daaab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when an agent needs web search results for Chinese, Taiwan, China, or East Asia topics, especially when ordinary search tools return weak Chinese-language coverage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to kaiwu.dev.

Mitigation: Install only when that data flow is acceptable for the intended use case.

Risk: The skill can attempt wallet-based registration for an API key.

Mitigation: Configure KAIWU_API_KEY manually when possible, and approve any SIWE wallet signature only after reviewing the message.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daaab/skills/kaiwu-search)
- [Kaiwu](https://kaiwu.dev)
- [Kaiwu search API endpoint](https://kaiwu.dev/v1/search)
- [Kaiwu credits API endpoint](https://kaiwu.dev/v1/credits)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires KAIWU_API_KEY for API calls; search responses include result titles, URLs, snippets, source engine, publication dates when available, and credit usage.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
