## Description: <br>
Provides health checkup report analysis, health risk summaries, personalized exercise plans, video recommendations, and daily check-in reminders from text, document, and OCR inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amitabhama](https://clawhub.ai/user/amitabhama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to parse health checkup data, summarize possible health risks, generate exercise and diet guidance, recommend exercise videos, and keep recurring check-in records. Its health guidance should be reviewed as informational support and not treated as professional medical advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive health data and stores local records. <br>
Mitigation: Install only where local health-data storage is acceptable, restrict file access, and review generated health guidance before acting on it. <br>
Risk: Scheduled reminders and broad auto-activation can send health-related messages without enough user intent. <br>
Mitigation: Require explicit user confirmation before enabling cron, heartbeat reminders, or outbound health-related messages, and narrow trigger phrases to intentional requests. <br>
Risk: Bundled Feishu credentials and embedded user or document identifiers may expose or misroute data. <br>
Mitigation: Remove and rotate bundled secrets, then replace embedded identifiers with per-user configuration before installation. <br>
Risk: Feishu or Tencent document flows may move health-related content through third-party services. <br>
Mitigation: Use those integrations only after confirming the destination workspace, document permissions, and user consent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/amitabhama/healthai) <br>
- [Health indicator reference ranges](references/指标参考范围.md) <br>
- [Calorie calculation reference](references/卡路里计算参考.md) <br>
- [Tencent Docs authorization reference](https://docs.qq.com/open/auth/mcp.html) <br>
- [Feishu developer platform](https://open.feishu.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, JSON-backed local records, and generated health tracking documents.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local health records, exercise plans, check-in files, online document content, and recurring reminder configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
