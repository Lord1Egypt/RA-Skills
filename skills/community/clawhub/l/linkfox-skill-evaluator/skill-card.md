## Description:

Evaluates agent skills for safety and effectiveness through static checks, prompt-based tests, assertions, transcript review, scoring, and recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lienong1122334](https://clawhub.ai/user/lienong1122334)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to evaluate whether an agent skill is safe to run and effective for its intended job. It guides the agent through pre-checks, safety review, test prompt design, assertion scoring, transcript review, and a final quality recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The evaluator reads supplied skill files and may run local pre-check behavior during assessment.

Mitigation: Use it on a specific skill directory or supplied artifact, and prefer an isolated environment before testing untrusted skills.

Risk: Testing untrusted skills can expose local files or credentials if the evaluated skill requests them.

Mitigation: Do not provide API keys, tokens, or credentials unless intentionally testing that part of the evaluated skill.

Risk: Evaluation reports can influence deployment decisions and may contain incorrect or misleading guidance.

Mitigation: Review the generated safety and quality findings before using them to approve, reject, or modify a skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lienong1122334/skills/linkfox-skill-evaluator)
- [Red Flag Details](artifact/references/red-flag-details.md)
- [Vertical Domain Review](artifact/references/vertical.md)
- [Process Flow Review](artifact/references/process-flow.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with assertion tables, risk findings, and recommendation text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local pre-check command examples and references to test artifacts or transcript evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
