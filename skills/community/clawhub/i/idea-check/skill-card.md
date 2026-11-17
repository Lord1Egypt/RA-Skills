## Description:

Provides a pre-build reality check for project ideas by scanning GitHub, Hacker News, npm, PyPI, and Product Hunt for similar existing work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spideystreet](https://clawhub.ai/user/spideystreet)

### License/Terms of Use:


## Use Case:

Developers, founders, and product builders use this skill to check whether a project idea already exists before investing in implementation. It helps an agent gather similarity signals, summarize competitors, and suggest pivot options from public software and product sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to run unpinned external tooling through mcporter and uvx.

Mitigation: Pin and verify the mcporter and uvx package sources before use, and run the tool in an isolated environment when practical.

Risk: Idea text may be sent to lookup services while checking for similar projects.

Mitigation: Avoid using confidential product plans unless the environment is approved and the user explicitly confirms that external checks are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spideystreet/skills/idea-check)
- [Publisher profile](https://clawhub.ai/user/spideystreet)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured competitor summaries, source lists, pivot hints, and inline shell commands for setup guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a reality signal score, top similar projects, checked sources, and setup instructions when required tooling is unavailable.]

## Skill Version(s):

1.0.0 (source: server release metadata and CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
