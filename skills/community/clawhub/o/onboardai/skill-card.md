## Description: <br>
AI新员工入职引导系统，覆盖入职前准备、首日引导、首周看板、30-60-90天成长路线、AI问答和满意度追踪，适用于HR和新人双角色的本地浏览器工作流。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
HR teams, new hires, buddies, and leaders use this skill to manage onboarding checklists, first-day guidance, weekly task tracking, 30-60-90 day milestones, employee Q&A, and onboarding satisfaction review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Real HR or employee records may be stored in browser localStorage or exported as local JSON. <br>
Mitigation: Use demonstration or non-sensitive data unless localStorage and local JSON exports are approved for the organization. <br>
Risk: Built-in onboarding examples may include access or WiFi/password-style instructions that are not appropriate for production use. <br>
Mitigation: Replace example access instructions with secure, authenticated onboarding flows such as SSO or one-time activation links. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/onboardai) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Onboarding dashboard asset](artifact/assets/onboarding-system.html) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Guidance] <br>
**Output Format:** [Interactive HTML dashboard with local browser state and JSON report export] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs as a single local HTML asset with browser localStorage persistence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
