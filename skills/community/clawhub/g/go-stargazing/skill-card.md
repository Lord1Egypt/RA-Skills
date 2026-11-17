## Description:

轻量版区域级拍星推荐技能，适用于今晚或指定日期的全国、省市级拍星条件筛选。默认全国扫描，先按云量粗筛，再结合真实天气细筛，输出逐晚推荐和完整气象信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[clhwbd](https://clawhub.ai/user/clhwbd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and photography planners use this skill to compare Chinese national, provincial, or city-level stargazing and Milky Way photography conditions for tonight or specified dates. It produces regional recommendations, backup options, weather details, and planning cautions rather than exact shooting locations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real-weather mode sends queried coordinates and dates to Open-Meteo.

Mitigation: Use the skill only when sharing those query details with Open-Meteo is acceptable, and disclose that dependency to users requesting real weather.

Risk: Unpinned Python dependencies can change behavior across installations.

Mitigation: Install in an isolated Python environment and pin or lock lunarcalendar and shapely before production use.

Risk: Regional forecasts, terrain effects, and reviewed accuracy concerns can make recommendations unsuitable as exact site decisions.

Mitigation: Present outputs as regional planning guidance, avoid treating them as specific camera-position recommendations, and recheck conditions before travel.

Risk: Open-Meteo failures, rate limits, or daily quota exhaustion can prevent fresh real-weather results.

Mitigation: Stop retrying after daily quota exhaustion, clearly tell the user that fresh weather cannot be fetched, and do not substitute mock data for real-weather conclusions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clhwbd/skills/go-stargazing)
- [Publisher profile](https://clawhub.ai/user/clhwbd)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Natural-language Chinese guidance or JSON results with regional rankings and weather details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are regional planning guidance; the skill does not produce Excel or xlsx exports.]

## Skill Version(s):

1.4.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
