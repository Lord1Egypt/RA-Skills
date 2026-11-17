## Description:

A Research plug bundle that groups Brave Search, data analysis, Python data visualization, and web crawler skills for search, analysis, visualization, and crawling workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and research analysts use this bundle to combine web search, data analysis, Python visualization, and web crawling into research and market-analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundle requests broad command execution and file read/write access across member skills.

Mitigation: Install and run it only in a controlled workspace with least-privilege file access, and review proposed commands or file changes before execution.

Risk: API credential and crawler behavior may be difficult to scope from the bundle alone.

Mitigation: Configure credentials only for the specific member skill that needs them, avoid sensitive local or private data, and set explicit crawling limits before use.

Risk: The release security summary classifies the bundle as suspicious because its scope is broad and credential guidance is inconsistent.

Mitigation: Perform a security review before installation and prefer a controlled research environment until stronger scoping is available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/plug-bundle-brave-search)
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, generated files, command output, and configuration guidance depending on the member skill used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May combine search results, analysis summaries, visualizations, crawl results, and integrated recommendations.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
