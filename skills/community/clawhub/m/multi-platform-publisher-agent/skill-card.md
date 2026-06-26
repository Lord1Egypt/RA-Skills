## Description: <br>
Helps agents prepare and manage multi-platform book publishing workflows, including platform-specific formatting, cover handling, publishing schedules, status tracking, and exception reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ouyang198000](https://clawhub.ai/user/ouyang198000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Authors, publishing operators, and automation developers use this skill to prepare manuscripts for Amazon KDP, 番茄小说, 起点中文网, 晋江文学城, Royal Road, 七猫小说, and similar platforms, then track publishing schedules, review status, platform IDs, links, and exceptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests authority over publishing accounts, desktop or browser automation, scheduling, and content submissions. <br>
Mitigation: Use only with explicit per-platform approval, least-privilege or temporary credentials, and manual review before submissions or scheduled publishing actions. <br>
Risk: CAPTCHA handling may involve third-party solver services and platform compliance concerns. <br>
Mitigation: Stop for human handling by default, or require separate informed consent before using any third-party CAPTCHA solver. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ouyang198000/multi-platform-publisher-agent) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with structured status data examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include platform publishing reports, book IDs, platform links, review status, schedule recommendations, and exception logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
