## Description:

基于惠迈校准框架的高考升学规划专家，三级校准+裂变定价+温情模式

This skill is ready for commercial/non-commercial use.

## Publisher:

[yezhaowang888-stack](https://clawhub.ai/user/yezhaowang888-stack)

### License/Terms of Use:

MIT-0

## Use Case:

External students, parents, and admissions-planning operators use this skill to produce Gaokao school recommendations, major-fit assessments, application strategy, and personalized planning reports. Promoters can also use its pricing guidance to structure paid service packages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect the agent environment and installed Skill list for compatibility checks.

Mitigation: Review before installation and restrict access to private installed-Skill lists through the host platform when that behavior is not acceptable.

Risk: The skill includes under-scoped memory-reuse guidance beyond ordinary admissions advice.

Mitigation: Install only where persistent memory access can be reviewed, disabled, or scoped to this admissions-planning use case.

Risk: Admissions recommendations may be incorrect or interpreted as enrollment guarantees.

Mitigation: Treat outputs as reference material, verify against official admissions data, and keep the skill's no-guarantee disclaimer visible to users.

Risk: The skill describes external DeepSeek API use for planning queries.

Mitigation: Use the host platform's configured API profile and review what query data is sent before enabling external service calls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yezhaowang888-stack/skills/prospect-advisor)
- [Skill Overview](artifact/SKILL.md)
- [Calibration Principles](artifact/calibration/principles.md)
- [Pricing Technical Plan](artifact/pricing/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include admissions recommendations, major assessments, application strategy reports, calibration results, pricing analysis, and install or configuration snippets.]

## Skill Version(s):

1.1.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
