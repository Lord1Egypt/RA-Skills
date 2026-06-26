## Description: <br>
Dual-purpose news intelligence system that searches recent news, extracts strategic patterns for an agent knowledge base, and generates CORE-analyzed personalized news briefings by category. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kedoupi](https://clawhub.ai/user/kedoupi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to run scheduled or ad hoc news scans, receive strategic Markdown briefings, and maintain local news logs plus selective concept and pattern notes. The skill is suited for personalized market, technology, policy, and business intelligence workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Personalized briefings can expose sensitive context from USER.md in local briefing content or logs. <br>
Mitigation: Keep USER.md limited to information appropriate for briefings and local logs, and periodically inspect or prune memory/news-log and memory/knowledge-base. <br>
Risk: Separate heartbeat, cron, Feishu, or other delivery integrations may introduce external-output or credential risks outside this skill. <br>
Mitigation: Review those integrations separately before enabling automated delivery, because this skill declares no direct external outputs or credentials. <br>
Risk: The skill depends on two other skills that shape analysis and news-source configuration. <br>
Mitigation: Review core-prism and news-source-manager before installation or production use. <br>


## Reference(s): <br>
- [ClawHub release: Insight Radar](https://clawhub.ai/kedoupi/insight-radar) <br>
- [Publisher profile: kedoupi](https://clawhub.ai/user/kedoupi) <br>
- [Category Configuration Guide](references/category-config.md) <br>
- [Category Recommendations](references/category-recommendations.md) <br>
- [Example Output Format](references/example-output.md) <br>
- [Dependency: core-prism](https://clawhub.ai/kedoupi/core-prism) <br>
- [Dependency: news-source-manager](https://clawhub.ai/kedoupi/news-source-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown briefing with category labels, source links, CORE analysis, cognitive digest entries, blind-spot questions, and optional local knowledge-base file updates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses built-in WebSearch and WebFetch, reads local user and news-source configuration, and writes local news logs and high-bar knowledge-base notes.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
