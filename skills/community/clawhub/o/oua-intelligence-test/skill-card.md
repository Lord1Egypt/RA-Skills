## Description:

OUA 统一智能评估 is a 10-dimension AI assessment framework for evaluating language understanding, reasoning, knowledge, coding, creativity, memory, tool use, safety, engineering delivery, and robustness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rafeyu8899](https://clawhub.ai/user/rafeyu8899)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, evaluators, and AI teams use this skill to run a structured 10-dimension assessment of AI model capabilities and reliability. It supports manual test administration, scoring, and report generation for model comparison and improvement planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTML reports generated from untrusted result JSON may embed unescaped content.

Mitigation: Generate and open HTML reports only from trusted result JSON until all report fields are safely escaped or a strict input schema is added.

## Reference(s):

- [OUA test bank](references/test-bank.md)
- [OUA scoring and report engine](scripts/score_test.py)
- [ClawHub skill page](https://clawhub.ai/rafeyu8899/skills/oua-intelligence-test)
- [Source repository link from artifact frontmatter](https://github.com/RafeYu8899/oua-intelligence-test)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON, HTML reports]

**Output Format:** [Markdown guidance with inline shell commands; generated reports may be HTML or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a 10-dimension assessment framework, test bank, scoring rubric, and report generator.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
