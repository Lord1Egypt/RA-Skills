## Description: <br>
Monitor Hong Kong IPO deadline and listing windows and return structured discovery results for near-term IPO scanning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hackstoic](https://clawhub.ai/user/hackstoic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to discover currently open Hong Kong IPO subscriptions, near-term subscription deadlines, and upcoming listings for downstream scanning or human summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled runtime includes broader IPO decision-support, profile, persistence, and suggestion-application features beyond the calendar monitor surface. <br>
Mitigation: Use only the documented calendar commands for calendar monitoring, and review profile, parameter, review, or suggestion files before relying on outputs. <br>
Risk: Runtime state or optional tokens may affect local execution. <br>
Mitigation: Set HKIPO_HOME to an isolated directory and avoid providing HKIPO_API_TOKEN unless necessary. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hackstoic/hkipo-calendar-monitor) <br>
- [hkipo-next README](runtime/hkipo-next/README.md) <br>
- [API Guide](runtime/hkipo-next/references/api-guide.md) <br>
- [AiPO API documentation](runtime/hkipo-next/references/aipo-api.md) <br>
- [IPO mechanism guide](runtime/hkipo-next/references/ipo-mechanism.md) <br>
- [Analysis guide](runtime/hkipo-next/references/analysis-guide.md) <br>
- [Risk preference guide](runtime/hkipo-next/references/risk-preferences.md) <br>
- [AiPO data source](https://aipo.myiqdii.com) <br>
- [AASTOCKS IPO data source](https://www.aastocks.com/tc/stocks/market/ipo/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [JSON, text, or Markdown CLI output; optional Markdown files when --output is used.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Calendar output includes IPO event items, data status, issue lists, and degraded-source metadata.] <br>

## Skill Version(s): <br>
0.1.0 (source: SKILL.md frontmatter, pyproject.toml, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
