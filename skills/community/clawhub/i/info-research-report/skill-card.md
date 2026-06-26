## Description: <br>
信息调研报告自动化工作流。一键完成：多源搜索、深度挖掘、政府风格 DOCX 报告生成和邮件发送。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zaferliu](https://clawhub.ai/user/zaferliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and OpenClaw users use this skill to turn search results or supplied source records into a formal Chinese DOCX research report and send it to a specified email recipient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically send generated reports by email and the security evidence notes a fallback to a fixed QQ address when no recipient is supplied. <br>
Mitigation: Run it only with an explicit, verified recipient email and review command arguments before execution. <br>
Risk: Webpage text and generated summaries may be sent to third-party LLM services and then transmitted by email. <br>
Mitigation: Avoid sensitive or regulated source material unless MiniMax or OpenAI processing and email transmission are approved for the use case; use dedicated API keys. <br>
Risk: Fetching untrusted source pages and resolving the external email skill can expand execution risk. <br>
Mitigation: Use --no-fetch for untrusted results and set OPENCLAW_SKILLS_DIR only to a trusted skills directory containing a trusted email-mail-master installation. <br>


## Reference(s): <br>
- [Skill README](README.md) <br>
- [Skill Definition](SKILL.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/zaferliu/info-research-report) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown usage guidance with shell commands; generated DOCX report file and email attachment when executed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a topic, recipient email, and optional results JSON; may fetch web content and call MiniMax or OpenAI when API keys are configured.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
