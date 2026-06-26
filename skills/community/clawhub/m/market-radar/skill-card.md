## Description: <br>
Industry hotspot and competitor monitoring across 5 dimensions for Chinese-language requests with competitor URLs, using international English sources to produce a structured Chinese daily brief with alerts and action recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[law52525](https://clawhub.ai/user/law52525) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Market intelligence, brand, and competitive research teams use this skill to monitor an industry and competitor websites, identify market signals, and receive a Chinese-language daily brief with alerts and role-based recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs an agent to browse public news, forum, industry, and competitor websites, which may expose the agent to untrusted web content. <br>
Mitigation: Use only intended competitor URLs and review the generated brief before relying on it for business decisions. <br>
Risk: Market signals and competitor observations may be incomplete when pages fail to load, block automation, or provide sparse public content. <br>
Mitigation: Preserve data quality notes in the report and treat inaccessible sources as coverage gaps rather than negative findings. <br>
Risk: The artifact references Telegram formatting, but the security evidence does not indicate that this package stores or sends credentials. <br>
Mitigation: Treat Telegram as output formatting or delivery context and avoid providing credentials unless the surrounding runtime explicitly requires and secures them. <br>


## Reference(s): <br>
- [Market Radar ClawHub page](https://clawhub.ai/law52525/market-radar) <br>
- [Monitoring rules](references/monitoring-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Chinese Markdown daily brief with tables, alerts, source notes, and action recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses agent-browser for public web browsing and formats the report for Telegram delivery context.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
