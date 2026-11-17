## Description:

美团外卖 helps an agent guide users through Meituan account authentication, claim Meituan coupon benefits, and query locally recorded coupon-claim history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meituan-openplatform](https://clawhub.ai/user/meituan-openplatform)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to claim available Meituan coupon benefits through an agent and to check prior coupon-claim records. The skill is intended for agents that can run local Python scripts, complete SMS-based login with user participation, and present coupon results clearly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Meituan phone login and reusable account/device tokens.

Mitigation: Use it only in isolated, single-user environments and confirm the user intentionally initiates SMS login before collecting phone numbers or verification codes.

Risk: Tokens can appear in script outputs, command arguments, or local history keys.

Mitigation: Avoid shared shells, command logging, transcript logging, and weakly isolated agent runtimes; review outputs before displaying or storing them.

Risk: Authentication and coupon history are persisted locally.

Mitigation: Use the documented environment variables to place token and history files in an isolated path, and clear login or device data when the user asks to reset access.

Risk: The artifact includes overreaching instructions that discourage inspection or parameter review.

Mitigation: Host agents and reviewers should ignore those instructions, inspect the scripts normally, and rely on platform policy and security review before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/meituan-openplatform/skills/meituan-takeout)
- [Meituan SMS login interface documentation](https://km.sankuai.com/collabpage/2752893495)
- [Publisher profile](https://clawhub.ai/user/meituan-openplatform)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline shell commands and JSON script outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-assisted Meituan SMS login; scripts may emit JSON containing account tokens and coupon data.]

## Skill Version(s):

1.0.4 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
