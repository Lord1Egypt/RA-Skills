## Description:

查询快递物流轨迹和签收状态，支持自动识别或手动指定快递公司，需配置快递100 API 凭据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[blueyan163-bot](https://clawhub.ai/user/blueyan163-bot)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up parcel tracking details through KuaiDi100, including current delivery state, recent tracking events, and supported courier companies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tracking numbers, courier codes, and any provided phone-number suffix are sent to KuaiDi100.

Mitigation: Use only with shipment data the user is allowed to share and with approved KuaiDi100 credentials.

Risk: Missing or invalid KuaiDi100 credentials prevent package lookup.

Mitigation: Configure credentials through environment variables and avoid embedding them in prompts or shared files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blueyan163-bot/skills/kauidi-express)
- [KuaiDi100 query API overview](https://www.kuaidi100.com/manager/v2/query/overview)
- [KuaiDi100 API site](https://www.kuaidi100.com/)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration]

**Output Format:** [JSON from a Python command-line helper, with tracking results, supported courier lists, or structured error responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires KUAIDI100_KEY and KUAIDI100_CUSTOMER environment variables; query inputs can include tracking number, courier code, and phone-number suffix.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
