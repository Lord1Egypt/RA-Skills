## Description: <br>
多目的地航线组合比价助手会收集出发地、旅行时间窗、候选城市和偏好，比较去程与回程城市组合并输出 Top 3 航线方案和路线建议。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[purelanren](https://clawhub.ai/user/purelanren) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-planning agents use this skill to compare multi-city flight options across candidate destinations, rank outbound and return city combinations, and produce concise itinerary recommendations with cost, transfer, duration, and route tradeoffs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to run FlyAI searches with HTTPS certificate validation disabled. <br>
Mitigation: Review commands before execution, prefer a version that keeps normal certificate validation enabled, and only run searches in a trusted environment. <br>
Risk: Travel searches may pass user travel constraints and preferences to an external FlyAI command-line tool. <br>
Mitigation: Use only after confirming the user is comfortable sharing the required trip details, and avoid entering unnecessary personal or payment information. <br>
Risk: Generated flight recommendations can become stale because prices, routes, and availability change quickly. <br>
Mitigation: Treat recommendations as planning guidance, recheck live booking sources before purchase, and clearly communicate that fares may change. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/purelanren/multi-city-flight-optimizer) <br>
- [FlyAI command reference](reference/flyai-commands.md) <br>
- [Tools guide](reference/tools-guide.md) <br>
- [Output templates](reference/output-templates.md) <br>
- [HTML visualization template](reference/html-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown recommendations with optional HTML file content and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask structured follow-up questions, generate a shareable HTML comparison file, and save travel preferences when the host environment provides those tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
