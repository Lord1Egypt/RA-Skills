## Description: <br>
关键词监控与内容采集自动化工具，用于多关键词并行监控、热门内容采集，并生成结构化日报推送到飞书群。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yesong-hue](https://clawhub.ai/user/yesong-hue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operations, competitive monitoring, trend tracking, and sales teams use this skill to monitor configured keywords, collect relevant public content, and receive structured Markdown reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Monitored topics, collected items, and generated reports may be sent to configured third-party search and Feishu/webhook services. <br>
Mitigation: Avoid sensitive or regulated keywords and confirm third-party data flow, retention expectations, and webhook destinations before deployment. <br>
Risk: The bundled privacy description says data is stored locally, while release security evidence flags conflicting external data flows. <br>
Mitigation: Treat local-only storage claims as unverified until the publisher documents how external search and report delivery are handled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yesong-hue/keyword-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/yesong-hue) <br>
- [Tavily API](https://tavily.com) <br>
- [AI智造工坊](http://ai.qnitgroup.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown reports and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include ranked items, titles, platforms, heat scores, publish times, and source links.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
