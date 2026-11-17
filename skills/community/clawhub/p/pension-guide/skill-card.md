## Description:

한국 국민연금, 퇴직금, 기초연금, IRP/연금저축, FIRE 질문을 분류하고 추정 계산과 안내 리포트를 생성합니다.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sw326](https://clawhub.ai/user/sw326)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to triage Korean pension and retirement-planning questions, estimate pension or severance-pay amounts, compare IRP and pension-savings tax effects, and produce informational planning guidance.

### Deployment Geography for Use:

South Korea

## Known Risks and Mitigations:

Risk: The skill includes guidance that could lead users to pass personal identifiers into a shell command.

Mitigation: Do not enter resident registration numbers or similar personal identifiers into shell commands; use official authenticated pension portals for exact personal estimates.

Risk: Pension, tax, and retirement calculations may be estimates or become outdated.

Mitigation: Treat calculations as informational planning estimates, verify current values with official sources, and do not treat responses as financial advice.

## Reference(s):

- [Intent Router](references/intent_router.md)
- [Output Templates](references/output_templates.md)
- [Source Tiers](references/source_tiers.md)
- [National Pension Service](https://www.nps.or.kr)
- [내연금](https://csa.nps.or.kr)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports with tables, estimates, disclaimers, and occasional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Flash responses are capped at 40 lines; deep-dive outputs are used for retirement simulation, IRP comparison, FIRE, severance pay, and pension-guide requests.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
