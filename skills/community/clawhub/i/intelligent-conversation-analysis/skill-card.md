## Description:

该技能调用阿里云晓蜜 CCAI AIO，对客服通话或文字对话进行 AI 智能分析，支持摘要生成、服务质检、情绪检测、满意度评估、关键词提取、字段抽取、QA 生成、用户画像、标签分类等任务，输入可以是文本对话或语音文件 URL。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuya-xyf](https://clawhub.ai/user/yuya-xyf)

### License/Terms of Use:

MIT-0

## Use Case:

Customer-support operations teams and developers use this skill to analyze pasted conversation text or public audio URLs for summaries, service quality review, sentiment and satisfaction signals, keyword and field extraction, QA pairs, user profiles, and tags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation text and audio URLs can contain sensitive customer or caller data and are sent to Alibaba Cloud CCAI for analysis.

Mitigation: Submit only data the user is authorized to process, redact unnecessary personal data, and confirm that Alibaba Cloud processing and retention terms are acceptable before execution.

Risk: The security summary flags under-scoped credential loading, which can expose broader Alibaba credentials than intended.

Mitigation: Use least-privilege, task-specific Alibaba Cloud credentials and keep unrelated secrets out of parent .env files.

Risk: Background polling and paid API calls can continue work or incur cost after task submission.

Mitigation: Use async polling only with an explicit stop condition, confirm requested result types before execution, and monitor API usage.

Risk: Audio analysis requires a reachable recording URL, and long-lived public URLs can broaden access to call recordings.

Mitigation: Prefer short-lived signed URLs or private access patterns and revoke recording access after analysis completes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuya-xyf/skills/intelligent-conversation-analysis)
- [Input format reference](references/input-formats.md)
- [CCAI AIO setup guide](references/setup.md)
- [Analysis type reference](references/task-types.md)
- [Troubleshooting guide](references/troubleshooting.md)
- [Alibaba Cloud CCAI AIO API documentation](https://help.aliyun.com/zh/model-studio/api-contactcenterai-2024-06-03-overview)
- [Alibaba Cloud App ID and Workspace ID guide](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON task configuration and shell commands; completed analysis is formatted text with raw JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports text dialogue and audio URL tasks; direct polling waits up to 120 seconds, while async mode returns a taskId for later query.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
