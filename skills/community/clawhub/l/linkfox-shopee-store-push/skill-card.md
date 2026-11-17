## Description:

Shopee（虾皮）Push 推送机制（与 linkfox-shopee-store-auth 同系列），经 /shopee/developerProxy 转发 Shopee Open API Push 模块全部 4 个接口：set_app_push_config、get_app_push_config、get_lost_push_message、confirm_consumed_lost_push_message。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operations teams use this skill to configure Shopee app push callbacks, inspect current push settings, retrieve lost push messages, and confirm consumed replay messages through LinkFox's Shopee gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill routes Shopee Push requests through LinkFox services.

Mitigation: Review before installing and use it only when the operator trusts LinkFox to process Shopee Push requests.

Risk: The skill stores full API responses locally.

Mitigation: Run it in a private workspace, review saved JSON before sharing logs or artifacts, and remove stored responses when they are no longer needed.

Risk: The skill handles login, API keys, phone verification codes, payments, and billing flows.

Mitigation: Avoid pasting phone codes or API keys into shared chats or logs, and prefer a proper secret store over shell profile files.

Risk: Gateway-related environment variables and SESSION_ID affect where requests are sent and where responses are stored.

Mitigation: Run the skill only in trusted environments and verify gateway variables and session identifiers before execution.

## Reference(s):

- [Shopee Push API Reference](references/api.md)
- [set_app_push_config](references/apis/set-app-push-config.md)
- [get_app_push_config](references/apis/get-app-push-config.md)
- [get_lost_push_message](references/apis/get-lost-push-message.md)
- [confirm_consumed_lost_push_message](references/apis/confirm-consumed-lost-push-message.md)
- [Authentication and Billing Onboarding](references/onboarding.md)
- [Shopee set_app_push_config documentation](https://open.shopee.com/documents/v2/v2.push.set_app_push_config?module=105&type=1)
- [Shopee get_app_push_config documentation](https://open.shopee.com/documents/v2/v2.push.get_app_push_config?module=105&type=1)
- [Shopee get_lost_push_message documentation](https://open.shopee.com/documents/v2/v2.push.get_lost_push_message?module=105&type=1)
- [Shopee confirm_consumed_lost_push_message documentation](https://open.shopee.com/documents/v2/v2.push.confirm_consumed_lost_push_message?module=105&type=1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON command inputs, and JSON API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts save full responses under a local linkfox session data directory and summarize large responses unless inline output is requested.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
