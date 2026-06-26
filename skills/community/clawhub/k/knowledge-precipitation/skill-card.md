## Description: <br>
知识自动沉淀引擎生成每日知识日志，汇总 Get笔记内容和 OpenClaw 对话记录，分析学习与工作状态，并归档到 configured Get笔记 and Feishu destinations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binhuatochina](https://clawhub.ai/user/binhuatochina) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and teams use this skill to turn daily notes and assistant conversations into a structured Markdown journal briefing with themes, analysis, keywords, and next-day focus. It is intended for users who want automated knowledge management across Get笔记 and Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads Get笔记 notes, OpenClaw conversation history, and stored service credentials. <br>
Mitigation: Install only in an environment where those data sources are intended for journaling, and review permissions before enabling the skill. <br>
Risk: The skill can publish full daily reports to configured Get笔记 and Feishu locations. <br>
Mitigation: Require a preview and explicit approval before cloud synchronization, permission changes, or external archive updates. <br>
Risk: Hardcoded Feishu folder, wiki node, app credential, and member identifiers may point to an unintended workspace or recipient. <br>
Mitigation: Verify every configured Feishu folder, wiki node, app credential, and member ID belongs to the intended account before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/binhuatochina/knowledge-precipitation) <br>
- [Briefing template](artifact/references/briefing-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown briefing with status text and generated archive links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local report files and synchronize full report content to configured Get笔记 and Feishu destinations.] <br>

## Skill Version(s): <br>
0.1.10 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
