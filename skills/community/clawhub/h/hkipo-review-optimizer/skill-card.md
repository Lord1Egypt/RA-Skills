## Description: <br>
Review past Hong Kong IPO decisions, update actual outcomes, export review datasets, and accept or reject tuning suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hackstoic](https://clawhub.ai/user/hackstoic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to review completed Hong Kong IPO decision records, capture actual outcomes, export review datasets, and manage accepted or rejected tuning suggestions for later scoring behavior. <br>

### Deployment Geography for Use: <br>
Global; the workflow is focused on Hong Kong IPO decision-support records. <br>

## Known Risks and Mitigations: <br>
Risk: The bundle includes a broader HK IPO decision-support runtime than the review-only description suggests. <br>
Mitigation: Install it only when the full HK IPO decision-support runtime is desired, not when a narrow review helper is sufficient. <br>
Risk: Profile data, review data, and exported datasets may contain sensitive decision history. <br>
Mitigation: Keep local data and exported review files out of shared directories and review export paths before writing files. <br>
Risk: Imported suggestions can change active scoring parameters. <br>
Mitigation: Import suggestions only from trusted files, preview changes first, and accept suggestions only after reviewing their effect. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hackstoic/hkipo-review-optimizer) <br>
- [Publisher profile](https://clawhub.ai/user/hackstoic) <br>
- [Runtime README](runtime/hkipo-next/README.md) <br>
- [Analysis guide](runtime/hkipo-next/references/analysis-guide.md) <br>
- [IPO mechanism reference](runtime/hkipo-next/references/ipo-mechanism.md) <br>
- [Risk preferences reference](runtime/hkipo-next/references/risk-preferences.md) <br>
- [API guide](runtime/hkipo-next/references/api-guide.md) <br>
- [AiPO API reference](runtime/hkipo-next/references/aipo-api.md) <br>
- [AiPO data source](https://aipo.myiqdii.com) <br>
- [AASTOCKS IPO market data](https://www.aastocks.com/tc/stocks/market/ipo/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Markdown, Text, Configuration guidance] <br>
**Output Format:** [Markdown instructions with CLI commands; runtime commands emit JSON, text, or markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses uv and local review storage at ~/.hkipo-next/data/hkipo.db.] <br>

## Skill Version(s): <br>
0.1.0 (source: SKILL.md frontmatter, pyproject.toml, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
