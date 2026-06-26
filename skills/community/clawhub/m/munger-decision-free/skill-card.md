## Description: <br>
Charlie Munger's mental model decision assistant analyzes decision scenarios, recommends relevant thinking models, and guides structured analysis for investment, product, strategy, and life decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cdz0451](https://clawhub.ai/user/cdz0451) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to apply a curated free set of 12 Munger-style mental models to concrete decisions. It supports scenario detection, model recommendation, guided questioning, and Markdown decision reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat investment percentages, action labels, or business and career recommendations as professional advice. <br>
Mitigation: Present outputs as heuristic prompts and require independent review before making financial, legal, career, or business decisions. <br>
Risk: Runtime or quality issues may occur because server security guidance notes that some referenced data files appear missing. <br>
Mitigation: Run the provided tests and verify required Node.js data files before relying on the skill in a workflow. <br>
Risk: The report generator uses simplified heuristics for scoring and recommendations. <br>
Mitigation: Review generated scores and recommendations against the original decision context instead of treating them as definitive conclusions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cdz0451/munger-decision-free) <br>
- [README-FREE.md](README-FREE.md) <br>
- [Skill instructions](SKILL.md) <br>
- [Munger model reference index](references/INDEX.md) <br>
- [Opportunity Cost](references/02-02-opportunity-cost.md) <br>
- [Circle of Competence](references/06-06-circle-of-competence.md) <br>
- [Margin of Safety](references/10-10-margin-of-safety.md) <br>
- [Confirmation Bias](references/12-12-confirmation-bias.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown prompts and decision-analysis reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports can include scenario labels, recommended models, heuristic scores, recommendations, and risk prompts.] <br>

## Skill Version(s): <br>
1.2.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
