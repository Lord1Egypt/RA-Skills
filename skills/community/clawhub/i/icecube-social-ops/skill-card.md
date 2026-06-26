## Description: <br>
IceCube Social Ops helps an agent plan and operate X/Twitter and Xiaohongshu social accounts, including login preparation, publishing schedules, engagement handling, and daily reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ares521521-design](https://clawhub.ai/user/ares521521-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and operators can use this skill to guide an agent through social account setup, content generation, scheduled publishing, engagement triage, and operational reporting for X/Twitter and Xiaohongshu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to use live social account sessions and may post, reply, follow, or handle direct messages publicly. <br>
Mitigation: Use an isolated browser profile containing only the intended accounts and require human draft review before posts, replies, follows, or direct messages. <br>
Risk: Autonomous operation could continue beyond the operator's intended platform, action, or timing boundaries. <br>
Mitigation: Define explicit platform, action, rate, schedule, and stop conditions before enabling autonomous operation. <br>
Risk: Stored or reusable browser sessions can expose sensitive social account access. <br>
Mitigation: Avoid saving reusable cookies and revoke or refresh sessions when account operation is complete. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ares521521-design/icecube-social-ops) <br>
- [ares521521-design Publisher Profile](https://clawhub.ai/user/ares521521-design) <br>
- [Xiaohongshu Creator Platform](https://creator.xiaohongshu.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with tables, checklists, schedules, reports, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include social post drafts, account operation checklists, engagement response guidance, and daily operations reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
