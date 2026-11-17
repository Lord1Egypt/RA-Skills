## Description:

Search the live web through Moonshot's builtin $web_search tool and return a concise answer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fusae](https://clawhub.ai/user/fusae)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to route live web search, current-information lookup, and online verification through Moonshot when page-level citation extraction is not required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search prompts are sent to Moonshot using the configured API key.

Mitigation: Do not submit sensitive private queries unless Moonshot's data handling is acceptable for the use case.

Risk: The skill returns a concise web-backed answer but may not provide exact citations or page-level source attribution.

Mitigation: Use a browser or search workflow when exact links, citations, or source inspection are required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fusae/skills/moonshot-web-search)
- [Publisher profile](https://clawhub.ai/user/fusae)
- [Project homepage](https://github.com/fusae/moonshot-search-skill)
- [Moonshot chat completions endpoint](https://api.moonshot.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text answer returned from a shell command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MOONSHOT_API_KEY and sends search prompts to Moonshot; use a browser/search workflow when exact citations or page-level attribution are required.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
