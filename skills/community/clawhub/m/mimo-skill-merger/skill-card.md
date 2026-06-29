## Description: <br>
技能合并器帮助代理分析多个技能的重叠和互补能力，并按吸收型、融合型或编排型策略生成合并方案与变更报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qqyougitcom](https://clawhub.ai/user/qqyougitcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to consolidate overlapping agent skills into a unified or orchestrated workflow while preserving source capabilities and documenting the resulting changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Merged skill output can change future agent trigger conditions and workflow routing. <br>
Mitigation: Review the generated merger report and scan any merged skill before using or publishing it. <br>
Risk: A consolidation proposal could omit source capabilities or leave conflicts unresolved. <br>
Mitigation: Use the required change comparison and boundary checks to confirm that all source skill capabilities remain covered. <br>


## Reference(s): <br>
- [skill-merger detailed reference](references/details.md) <br>
- [ClawHub skill page](https://clawhub.ai/qqyougitcom/mimo-skill-merger) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Chinese Markdown merger report with proposed SKILL.md frontmatter and workflow sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a change comparison and should be reviewed before using or publishing merged skills.] <br>

## Skill Version(s): <br>
1.3.0 (source: SKILL.md frontmatter and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
