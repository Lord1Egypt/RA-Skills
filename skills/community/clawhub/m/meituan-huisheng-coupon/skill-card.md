## Description: <br>
Helps users claim Meituan coupons and check same-day promotional activity across Meituan-covered local services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fhao233](https://clawhub.ai/user/fhao233) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Meituan users use this skill to claim available coupons, view current promotions, complete account authorization when needed, and optionally manage daily coupon reminders. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The security scan verdict is suspicious because the skill includes under-disclosed authentication, device-fingerprinting, global HTTP-patching, scheduled automation, and self-updating background components. <br>
Mitigation: Install only if the publisher is trusted and these behaviors are acceptable; prefer waiting for clearer documentation or a narrower implementation. <br>
Risk: The skill can store Meituan login tokens and device identifiers locally. <br>
Mitigation: Use it only in a trusted local environment, avoid sharing diagnostic logs, and use the logout or device-reset flows when access should be removed. <br>
Risk: Optional scheduled coupon claiming can perform repeated account actions without a fresh prompt each day. <br>
Mitigation: Enable scheduled reminders only deliberately, verify the configured time, and disable the schedule when ongoing automation is no longer wanted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fhao233/meituan-huisheng-coupon) <br>
- [Doctor guide](references/DOCTOR.md) <br>
- [Skill service terms](references/terms-of-service.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown and short user-facing status messages, with JSON consumed internally from local scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May display a login QR image or link, coupon tables, promotion links, scheduled reminder confirmations, and diagnostic summaries.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
