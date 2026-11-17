## Description:

Evaluate LLM agents using behavioral tests, capability assessments, reliability metrics, and benchmarks to identify real-world performance issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godferylindsay](https://clawhub.ai/user/godferylindsay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quality engineers use this skill to design and run evaluations for LLM agents, including behavioral regression tests, capability assessments, adversarial tests, reliability metrics, and benchmark analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Evaluation messages, prompts, traces, user conversations, or benchmark data may be sent to SkillBoss when following the API integration example.

Mitigation: Use synthetic or redacted test data unless the organization has approved sending production or confidential evaluation data to SkillBoss.

Risk: Evaluation data can leak into prompts, training examples, or benchmark-tuned workflows and make results look stronger than real production behavior.

Mitigation: Keep test sets separated from prompts and training data, and validate results with production-like behavioral and adversarial tests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/godferylindsay/skills/martin-agent-evaluation)
- [ClawHub publisher profile](https://clawhub.ai/user/godferylindsay)
- [SkillBoss setup guide](https://skillboss.co/skill.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with evaluation patterns, risk notes, and Python API examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request examples that require SKILLBOSS_API_KEY.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
