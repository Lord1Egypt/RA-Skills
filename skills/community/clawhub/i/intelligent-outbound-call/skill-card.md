## Description:

晓蜜智能外呼 helps agents prepare, launch, and monitor Alibaba Cloud Xia蜜 outbound call campaigns for scenarios such as customer notices, satisfaction surveys, interview invitations, reminders, and CRM-driven follow-up.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuya-xyf](https://clawhub.ai/user/yuya-xyf)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to configure outbound-call campaigns, validate recipient lists, generate task input, start Alibaba Cloud Xia蜜 calls, and query campaign progress or call results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can start real bulk outbound calls.

Mitigation: Use a human confirmation step before execution, verify caller-number authorization, and confirm recipient consent or another valid legal basis for the campaign.

Risk: Alibaba Cloud credentials could grant broader calling or data access than the task requires.

Mitigation: Install and run the skill only with least-privilege Alibaba Cloud credentials dedicated to approved outbound-calling workflows.

Risk: Recipient contact data and business context may include sensitive personal data.

Mitigation: Provide only the minimum required phone, name, scenario, and agentProfile.background data; avoid whole CRM records, resumes, order histories, and sensitive notes.

Risk: Call recordings and signed download links may expose personal data.

Mitigation: Treat recordings and signed recording URLs as sensitive, limit access, and avoid sharing them outside approved review or support workflows.

## Reference(s):

- [Input Formats](artifact/references/input-formats.md)
- [Phone Number Setup](artifact/references/phone-number-setup.md)
- [Common Scenarios](artifact/references/scenarios.md)
- [Troubleshooting](artifact/references/troubleshooting.md)
- [Alibaba Cloud Xia蜜 Console](https://outboundbot.console.aliyun.com/)
- [Alibaba Cloud Xia蜜 Documentation](https://help.aliyun.com/product/outboundbot.html)
- [Alibaba Cloud Communication Line Application](https://help.aliyun.com/zh/outboundbot/product-overview/apply-for-a-communication-line)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON task input and shell commands; command output includes JSON or text status for call jobs, query results, and recording links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce taskInput.json structure, Alibaba Cloud job group IDs, instance IDs, script IDs, call counts, job status summaries, and signed recording download metadata.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
