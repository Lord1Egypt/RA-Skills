## Description: <br>
Monitors public trending-topic sources, scores topics for relevance and writability, drafts initial topic angles, writes selected records to Feishu, and prepares Telegram-ready recommendation text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytearch1990-beep](https://clawhub.ai/user/bytearch1990-beep) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators and publishing teams use this skill to discover current AI, technology, productivity, and creator-economy topics, rank them, and turn high-scoring items into structured topic records and recommendation messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Feishu app and table credentials to write topic records. <br>
Mitigation: Provide credentials only through environment variables, scope the Feishu app to the intended workspace and table, and verify the configured destination before running. <br>
Risk: Scheduled or daemon mode can repeatedly fetch public trend sites and retain topic-planning outputs in local database, log, and temporary files. <br>
Mitigation: Use recurring modes only when continuous collection is intended, monitor generated logs and databases, and remove stored outputs according to the workspace retention policy. <br>
Risk: Automated trend scoring can surface noisy or misleading public topics as recommendations. <br>
Mitigation: Review selected topics, source context, and generated angles before publishing or handing them to downstream writing workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Release](https://clawhub.ai/bytearch1990-beep/inkroam-topic-expert) <br>
- [TopHub](https://tophub.today/) <br>
- [Feishu Open API](https://open.feishu.cn/open-apis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, code] <br>
**Output Format:** [Markdown-style recommendation text, JSON run summaries, Feishu records, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores topic records locally and can write selected topic data to configured Feishu tables.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
