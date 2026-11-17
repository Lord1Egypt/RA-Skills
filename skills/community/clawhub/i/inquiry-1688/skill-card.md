## Description:

Submits inquiry questions to 1688 suppliers through AlphaShop, checks results after about 20 minutes, and delivers summarized supplier replies through DingTalk or a fallback result file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

External commerce and procurement users use this skill to ask 1688 suppliers about price, minimum order quantity, customization, logistics, certifications, specifications, samples, and related purchasing questions. It helps an agent submit the inquiry, track the task, and return supplier answers after the delayed lookup completes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inquiry results can be automatically sent to fixed DingTalk target 238382.

Mitigation: Install only if that target is the intended recipient for all results; prefer a release that routes replies dynamically and stores requester identity with each task.

Risk: Delayed scheduled-agent instructions can run result-delivery steps after the original user interaction.

Mitigation: Review scheduled delivery behavior before use, confirm submissions with users, and restrict the skill to trusted workspaces with the required AlphaShop credentials.

Risk: Dependency ranges are not pinned exactly.

Mitigation: Pin and review dependencies before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1688aiinfra/skills/inquiry-1688)
- [1688aiinfra publisher profile](https://clawhub.ai/user/1688aiinfra)
- [AlphaShop API key management](https://www.alphashop.cn/seller-center/apikey-management)
- [AlphaShop API credits](https://www.alphashop.cn/seller-center/home/api-list)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets and JSON API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit AlphaShop API requests, schedule delayed result checks, and deliver inquiry summaries through DingTalk or local result files.]

## Skill Version(s):

1.0.2 (source: server evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
