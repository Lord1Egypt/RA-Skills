## Description: <br>
该技能调用阿里云晓蜜 CCAI AIO，对客服通话或文字对话进行 AI 智能分析，支持摘要生成、服务质检、情绪检测、满意度评估、关键词提取、字段抽取、QA 生成、用户画像、标签分类等多种分析任务，输入可以是文本对话或语音文件 URL。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuya-xyf](https://clawhub.ai/user/yuya-xyf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Customer service and operations teams use this skill to analyze support conversations or call recordings for summaries, quality inspection, sentiment, satisfaction, keywords, structured fields, QA pairs, user profiles, and classification tags. Agents can use it to prepare Alibaba Cloud CCAI AIO tasks from text conversations or public audio URLs and return the analysis results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use local Alibaba Cloud credentials. <br>
Mitigation: Use a dedicated least-privilege RAM credential and avoid broad ContactCenterAI:* permissions where possible. <br>
Risk: Customer conversations or recordings may be sent to Alibaba Cloud CCAI AIO for analysis. <br>
Mitigation: Minimize or redact sensitive data before submission, especially for customer, financial, health, or regulated conversations. <br>
Risk: The documented async polling flow can continue background result checks. <br>
Mitigation: Supervise or disable async cron polling unless retries are bounded and pending checks can be cancelled. <br>


## Reference(s): <br>
- [Input Formats](references/input-formats.md) <br>
- [Setup Guide](references/setup.md) <br>
- [Task Types](references/task-types.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Aliyun CCAI AIO API Documentation](https://help.aliyun.com/zh/model-studio/api-contactcenterai-2024-06-03-overview) <br>
- [Aliyun App ID and Workspace ID Guide](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON task configuration and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Alibaba Cloud CCAI AIO task setup guidance and formatted conversation analysis results; text inputs are documented with a 20,000 character limit and async polling is supported.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
