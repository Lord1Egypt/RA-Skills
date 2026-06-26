## Description: <br>
基于惠迈校准框架的高考升学规划专家，三级校准+裂变定价+温情模式。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yezhaowang888-stack](https://clawhub.ai/user/yezhaowang888-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, parents, and education advisors use this skill to generate gaokao college recommendations, major-fit assessments, application strategies, and personalized planning reports. Promoters may also use its pricing and redemption-code materials for paid advisory distribution. <br>

### Deployment Geography for Use: <br>
China-focused; usable globally where gaokao admissions planning is relevant. <br>

## Known Risks and Mitigations: <br>
Risk: Pricing materials describe identity tracking, payments, referral attribution, redemption codes, and commission settlement that are not reconciled with the privacy claims. <br>
Mitigation: Clarify what personal identifiers, payment records, referral data, and redemption-code data are collected or stored; document access, consent, deletion, refund, and dispute processes before commercial use. <br>
Risk: The skill requires sensitive external service credentials for model access. <br>
Mitigation: Store API keys only in the platform's credential profile mechanism, avoid embedding secrets in skill files or prompts, and rotate any exposed credentials. <br>
Risk: Admissions recommendations can be incomplete, outdated, or misinterpreted as a guarantee. <br>
Mitigation: Present outputs as advisory, keep the no-guarantee disclaimer visible, and require users to verify decisions against official admissions sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yezhaowang888-stack/prospect-advisor) <br>
- [Skill overview](artifact/SKILL.md) <br>
- [Calibration principles](artifact/calibration/principles.md) <br>
- [Pricing technical plan](artifact/pricing/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with structured recommendations, reports, and JSON configuration examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May depend on OpenClaw Gateway, a configured DeepSeek API profile, and platform-provided historical admissions data.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and artifact/_meta.json; artifact/package.json lists 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
