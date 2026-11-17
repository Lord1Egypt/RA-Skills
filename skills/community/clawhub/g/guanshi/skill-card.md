## Description:

观势 is a Chinese-language strategy-analysis agent that turns business strategy questions into structured BLM-based market, competition, organization, growth, and implementation reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuobadaidai](https://clawhub.ai/user/tuobadaidai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and strategy teams use this skill for strategic analysis, market and industry research, competitive positioning, business-model evaluation, growth strategy, transformation planning, and organization-strategy fit diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The initializer can persistently install remote companion skills into the local agent environment.

Mitigation: Review the initializer before running it, avoid --yes unless remote skill installation is intended, and use --skip-agents when only local knowledge-base templates are needed.

Risk: Strategic-analysis workflows may use external web search and may save report-derived PPT outline files under output/.

Mitigation: Do not provide confidential company data unless external search and local report-derived files are acceptable; review generated outputs before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tuobadaidai/skills/guanshi)
- [Skill definition](artifact/SKILL.md)
- [Core principles](artifact/references/core-principles.md)
- [Enterprise lifecycle model](artifact/references/lifecycle-model.md)
- [Six-step insight method](artifact/references/six-steps.md)
- [Strategy frameworks](artifact/references/strategy-frameworks.md)
- [Scenario routing](artifact/references/scenario-routing.md)
- [Expert registry](artifact/references/expert-registry.md)
- [Scheduling protocol](artifact/references/scheduling-protocol.md)
- [Audit checklist](artifact/references/audit-checklist.md)
- [Logic audit checklist](artifact/references/logic-audit-checklist.md)
- [Iteration self-check](artifact/references/iteration-selfcheck.md)
- [Output specification](artifact/references/output-spec.md)
- [PPT bridge protocol](artifact/references/ppt-bridge-protocol.md)
- [Supplementary notes](artifact/references/supplementary.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown strategic reports, with optional JSON PPT outline files for medium and complex analyses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save report-derived PPT outline data under output/; initializer can create local knowledge-base template files and install companion expert skills.]

## Skill Version(s):

3.2.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
