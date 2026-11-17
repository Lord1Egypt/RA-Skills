## Description:

美团外卖红包 helps agents guide users through Meituan account authentication, coupon collection, coupon-history lookup, and optional scheduled daily coupon collection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meituan-openplatform](https://clawhub.ai/user/meituan-openplatform)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill through an agent to collect Meituan coupons, authenticate a Meituan account when needed, review prior coupon records, and optionally set up recurring daily coupon collection.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill uses real Meituan account login and stores local user_token and device_token values.

Mitigation: Install only when comfortable with the Meituan phone/SMS login flow, avoid shared machines, and clear login or device data when no longer needed.

Risk: The recurring automatic coupon feature can repeatedly act on the user's account with weak scoping.

Mitigation: Review the scheduled coupon behavior before enabling it, disable the recurring task when it is not wanted, and confirm the schedule uses Beijing time.

Risk: Generated logs or process output may expose full token values.

Mitigation: Treat logs and command output as sensitive, do not share raw outputs, and redact token values before troubleshooting.

## Reference(s):

- [Authentication flow](artifact/references/auth-flow.md)
- [Scheduled coupon collection rules](artifact/references/cron-rules.md)
- [Response templates](artifact/references/response-copy.md)
- [ClawHub skill page](https://clawhub.ai/meituan-openplatform/skills/meituan-waimai-coupon)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown-like Chinese user responses with script-backed JSON results and inline shell commands for agent execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include coupon details, authentication prompts, scheduled-task setup messages, and error handling guidance; full tokens should not be displayed.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
