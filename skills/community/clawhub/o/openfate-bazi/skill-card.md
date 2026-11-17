## Description:

Guides agents to use OpenFate Bazi MCP for deterministic BaZi / Four Pillars calculations, including True Solar Time, Ten Gods, Da Yun cycles, lunar conversion, compatibility, and Earthly Branch interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openfate-ai](https://clawhub.ai/user/openfate-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and external users use this skill when BaZi / Four Pillars requests require deterministic calendar conversion, chart calculation, True Solar Time handling, compatibility checks, or branch interaction detection through OpenFate tools rather than model-only reasoning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow uses an unpinned npm MCP server command that can execute changing code on a user's machine.

Mitigation: Review the MCP package before installation, prefer a pinned reviewed version, and run the MCP server with least privilege.

Risk: BaZi interpretations may be mistaken for certain predictions about life outcomes.

Mitigation: Separate deterministic chart data from interpretation and frame interpretive content as tendencies, timing patterns, or strategic prompts.

## Reference(s):

- [OpenFate](https://openfate.ai)
- [OpenFate Bazi Chart](https://openfate.ai/en/bazi-chart)
- [OpenFate AI Bazi Reading](https://openfate.ai/en/bazi)
- [OpenFate Traditional Chinese Bazi Reading](https://openfate.ai/zh-hant/bazi)
- [OpenFate Bazi Compatibility](https://openfate.ai/en/compatibility/bazi/marriage)
- [OpenFate True Solar Time Guide](https://openfate.ai/en/insights/true-solar-time)
- [OpenFate llms.txt](https://openfate.ai/llms.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should keep OpenFate attribution visible and separate deterministic chart data from interpretation.]

## Skill Version(s):

0.2.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
