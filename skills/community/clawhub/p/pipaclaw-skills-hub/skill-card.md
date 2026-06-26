## Description: <br>
Front door for Pipaclaw public skills that routes users to the right skill for presentations, social account operations, and promotional video production without making them choose implementation details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xexojay](https://clawhub.ai/user/xexojay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this hub to route broad requests into the right public workflow: presentation creation, Xiaohongshu/X/Douyin account operations, or promotional video production. It is useful when the user knows the desired outcome but should not need to choose a sub-skill or implementation path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The promo-video workflow contacts nano.djdog.ai, sends the machine hostname during provisioning, and stores an API key under ~/.config/maliang-hub. <br>
Mitigation: Review this behavior before installing, and avoid running bootstrap or API helper scripts if that network and credential behavior is not acceptable for the environment. <br>
Risk: Helper scripts can send selected local file contents or JSON payloads to the video service and can initiate quote, task, and polling API calls. <br>
Mitigation: Only pass files and request bodies intended for the service, inspect generated quotes before paid execution, and keep customer material out of the public skill package. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xexojay/pipaclaw-skills-hub) <br>
- [Routing Map](references/routing-map.md) <br>
- [PPT Maker](ppt-maker/SKILL.md) <br>
- [Promo Video Maker](promo-video-maker/SKILL.md) <br>
- [Social Account Ops](social-account-ops/SKILL.md) <br>
- [Promo Video Artifact Contracts](promo-video-maker/references/artifact-contracts.md) <br>
- [Social Platform Playbook](social-account-ops/references/platform-playbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, structured status blocks, shell commands, JSON API responses, and generated file or URL handoffs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May route to presentation plans and files, social account operating drafts, promo video quotes, task receipts, workspace links, or helper-script commands depending on the selected public skill.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
