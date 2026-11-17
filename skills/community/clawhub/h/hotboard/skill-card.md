## Description:

OpenClaw skill for fetching hot trending data from multiple platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[llnancy](https://clawhub.ai/user/llnancy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Hotboard to select relevant trend platforms and fetch current hot lists with the hotboard CLI. It supports platform-specific parameters and Markdown or JSON output for trend discovery across news, technology, developer, entertainment, sports, reading, international, and utility sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the hotboard PyPI CLI, so installing it introduces ordinary third-party package supply-chain risk.

Mitigation: Use a pinned or internally reviewed package version before enabling it in agent environments.

Risk: The CLI fetches trending-topic data from external platforms, so returned items may be volatile, incomplete, or unsuitable for sensitive workflows.

Mitigation: Review returned topics before using them in downstream actions, and run the skill in a restricted environment when agents have access to sensitive files, credentials, or network resources.

## Reference(s):

- [Hotboard ClawHub skill page](https://clawhub.ai/llnancy/skills/hotboard)
- [hotboard PyPI package](https://pypi.org/project/hotboard/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with hotboard CLI commands and optional Markdown or JSON trend results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports platform-specific parameters such as GitHub time range, Baidu search type, Bilibili category, Douban list type, and earthquake filters.]

## Skill Version(s):

0.0.1 (source: target metadata and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
