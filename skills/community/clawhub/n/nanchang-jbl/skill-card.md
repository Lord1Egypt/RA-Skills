## Description: <br>
Nanchang Jbl is a customer-service skill for Nanchang Carpoly paint and coatings inquiries, covering product guidance, promotions, construction service information, after-sales routing, and store recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liubuq-sys](https://clawhub.ai/user/liubuq-sys) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External customers and store staff use this skill to answer paint, coating, renovation, construction, promotion, after-sales, and nearby-store questions for Nanchang Carpoly and Jiangxi Taolejia retail scenarios. <br>

### Deployment Geography for Use: <br>
China (Nanchang, Jiangxi focused) <br>

## Known Risks and Mitigations: <br>
Risk: Installers configure persistent daily auto-updates from a remote repository through cron or Windows Task Scheduler. <br>
Mitigation: Prefer the ClawHub install path or a manually reviewed install, and remove or disable the scheduled auto-update task if recurring remote updates are not desired. <br>
Risk: Auto-updates can replace the skill directory with newly fetched content. <br>
Mitigation: Review updates before deployment and pin or manually update the skill in environments that require change control. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/liubuq-sys/nanchang-jbl) <br>
- [Publisher profile](https://clawhub.ai/user/liubuq-sys) <br>
- [Business information](references/business-info.md) <br>
- [Services](references/services.md) <br>
- [Recommendations](references/recommendations.md) <br>
- [Promotions](references/promotions.md) <br>
- [After-sales](references/after-sales.md) <br>
- [Construction](references/construction.md) <br>
- [Stores](references/stores.md) <br>
- [Brand](references/brand.md) <br>
- [Images](references/images.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Conversational text or Markdown grounded in local reference files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Business details, prices, promotions, and store information should be treated as reference-grounded and subject to store confirmation.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
