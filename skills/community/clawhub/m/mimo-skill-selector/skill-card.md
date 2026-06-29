## Description: <br>
技能选择器 helps a Chinese-speaking agent choose the most relevant installed skills by matching user intent with keywords and semantic similarity, then returning a ranked Top 3 recommendation with reasons and use cases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qqyougitcom](https://clawhub.ai/user/qqyougitcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they have many installed skills and need the agent to recommend the best fit for a task. It is intended for skill-selection guidance, including ranking up to three installed skills, explaining why each is relevant, and asking clarifying questions for vague requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate on broad skill-choice phrasing and recommend another skill that is not the best fit. <br>
Mitigation: Review the ranked recommendations and reasons before allowing the agent to load or act through the selected skill. <br>
Risk: The skill only recommends installed skills, so it may miss better options that are not currently installed. <br>
Mitigation: Treat unmatched or partial matches as selection guidance and separately search or install additional skills when coverage is insufficient. <br>


## Reference(s): <br>
- [Skill details](references/details.md) <br>
- [ClawHub skill page](https://clawhub.ai/qqyougitcom/mimo-skill-selector) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/qqyougitcom) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Chinese Markdown-style ranked recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns up to three installed-skill recommendations with reasons and short use-case notes; may ask one or two clarifying questions for vague requests.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
