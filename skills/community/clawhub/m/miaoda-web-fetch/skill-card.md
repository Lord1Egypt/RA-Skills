## Description:

Helps an agent fetch a user-specified URL with `miaoda-studio-cli web-crawl` and summarize or extract the page content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nice1234-h](https://clawhub.ai/user/nice1234-h)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when a user provides a specific web page URL and needs the agent to fetch, summarize, or extract content. It also guides the agent to use search first when no specific URL is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can cause an agent to fetch web pages through `miaoda-studio-cli`.

Mitigation: Use it only for URLs intended to be retrieved, and prefer the search skill when the user does not already have a specific URL.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nice1234-h/skills/miaoda-web-fetch)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands; fetched page output can be text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a specific URL; JSON output is available with `--output json`.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
