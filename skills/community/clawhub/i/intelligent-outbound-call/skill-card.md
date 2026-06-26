## Description: <br>
该技能调用阿里云晓蜜外呼机器人，向指定手机号码列表发起自动语音外呼，支持自定义话术场景、批量号码处理和任务进度追踪。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuya-xyf](https://clawhub.ai/user/yuya-xyf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business users and operators use this skill to launch Alibaba Cloud Xiaomi outbound voice campaigns for notifications, surveys, callbacks, interview invitations, and activity reminders after reviewing recipient lists and call context. <br>

### Deployment Geography for Use: <br>
Mainland China <br>

## Known Risks and Mitigations: <br>
Risk: The skill can start real Alibaba Cloud outbound call campaigns at scale, which can incur costs and contact many recipients. <br>
Mitigation: Use a dedicated least-privilege Alibaba Cloud key, test with a small recipient list first, and confirm the exact phone list before execution. <br>
Risk: Outbound calls may involve personal phone numbers and business context sent to Alibaba Cloud. <br>
Mitigation: Verify consent and legal compliance, share only necessary call background, and review the call context before confirming execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuya-xyf/intelligent-outbound-call) <br>
- [Input formats](references/input-formats.md) <br>
- [Phone number setup](references/phone-number-setup.md) <br>
- [Common scenarios](references/scenarios.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Alibaba Cloud Xiaomi Outbound Bot console](https://outboundbot.console.aliyun.com/) <br>
- [Alibaba Cloud Xiaomi Outbound Bot documentation](https://help.aliyun.com/product/outboundbot.html) <br>
- [Alibaba Cloud outbound line application process](https://help.aliyun.com/zh/outboundbot/product-overview/apply-for-a-communication-line) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, JSON, Shell commands, Text] <br>
**Output Format:** [Markdown guidance with JSON configuration and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create taskInput.json and return Alibaba Cloud instance IDs, job group IDs, outbound call counts, and progress summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
