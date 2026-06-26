## Description: <br>
美团红包助手 helps users claim Meituan coupons and red-packet offers across supported Meituan categories and query coupon claim history after Meituan account authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meituan-openplatform](https://clawhub.ai/user/meituan-openplatform) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill through an agent to authenticate with Meituan, claim eligible coupons, view coupon claim records, and optionally configure daily automatic coupon claiming. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores reusable Meituan login tokens and local coupon history for repeat use. <br>
Mitigation: Install only when the publisher is trusted, prefer an isolated workspace, and clear stored authentication or device data when finished. <br>
Risk: The skill can configure recurring automatic coupon claiming, which may perform ongoing account actions. <br>
Mitigation: Enable auto-claim only when the user explicitly wants ongoing actions, and review or cancel scheduled tasks when no longer needed. <br>
Risk: The security evidence flags shared local cache behavior that users should review before installation. <br>
Mitigation: Use an isolated workspace for sensitive accounts and remove stored cache files after use if persistence is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/meituan-openplatform/meituan-coupon) <br>
- [Authentication flow](artifact/references/auth-flow.md) <br>
- [Scheduled auto-claim rules](artifact/references/cron-rules.md) <br>
- [Response copy templates](artifact/references/response-copy.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with shell command invocations and JSON script results handled by the agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include coupon status tables, login prompts, scheduled-task setup guidance, and error messages.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
