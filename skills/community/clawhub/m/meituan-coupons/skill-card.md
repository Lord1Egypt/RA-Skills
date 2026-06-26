## Description: <br>
A Meituan coupon assistant that helps users authenticate, claim coupons and red packets across Meituan categories, query claim history, and optionally set daily scheduled claiming. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meituan-skillhub](https://clawhub.ai/user/meituan-skillhub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to claim Meituan coupons or red packets, check prior claim records, manage Meituan login state, and configure optional daily coupon claiming. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Meituan login tokens and may store credentials locally, in shared cache, or across sessions. <br>
Mitigation: Install only if the publisher is trusted, prefer the documented --auto flow, avoid agent-memory token storage unless explicitly wanted, and clear login and device tokens when no longer using the skill. <br>
Risk: The skill can configure daily scheduled account actions. <br>
Mitigation: Review scheduled jobs before enabling them, disable cron jobs when they are no longer needed, and confirm that scheduled claiming matches the user's intent. <br>
Risk: The security review notes a background Node signing/update component that users should review carefully. <br>
Mitigation: Review the installed artifact behavior before use and install only when comfortable with the signing or update component described by the security guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/meituan-skillhub/meituan-coupons) <br>
- [Authentication flow](references/auth-flow.md) <br>
- [Scheduled claiming rules](references/cron-rules.md) <br>
- [Response copy templates](references/response-copy.md) <br>
- [Meituan coupon service rules](https://open-pepper.meituan.com/eds/rules/meituan-coupon-skill-service-rule.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Configuration, Guidance] <br>
**Output Format:** [Markdown user-facing messages, shell command invocations, and JSON script results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform authenticated Meituan account actions, persist local or shared tokens, and configure daily scheduled coupon claiming when enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
