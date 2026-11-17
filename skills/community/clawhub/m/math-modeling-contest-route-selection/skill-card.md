## Description:

Select superior mathematical modeling contest problems and modeling-solution routes for CUMCM A/B/C, MCM, ICM, and similar contests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[y3519712124-ui](https://clawhub.ai/user/y3519712124-ui)

### License/Terms of Use:

MIT-0

## Use Case:

External contest participants, students, and modeling teams use this skill to compare CUMCM A/B/C, MCM, ICM, and similar problem choices, then select feasible modeling routes with baselines, validation plans, fallback triggers, and paper-ready justification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent to run a bundled Python scoring script that writes a Markdown report when an output path is provided.

Mitigation: Run the script only in workspaces where creating contest-planning files is acceptable, and review the output path before execution.

## Reference(s):

- [Award Method Distillation](references/award-method-distillation.md)
- [Award-Style Question Decomposition](references/award-question-decomposition.md)
- [Award Route Pattern Library](references/award-route-pattern-library.md)
- [Contest Archives And Historical Scope](references/contest-archives.md)
- [Engineering Feasibility For Modeling Routes](references/engineering-feasibility.md)
- [Method Map](references/method-map.md)
- [Paper Scoring Framework](references/paper-scoring-framework.md)
- [Problem Taxonomy For Topic Selection](references/problem-taxonomy.md)
- [Refutation And Model-Choice Workflow](references/refutation-and-model-choice.md)
- [Topic And Method Route Selection Rubric](references/selection-rubric.md)
- [CUMCM official site](https://www.mcm.edu.cn/)
- [CUMCM historical problem archive](https://www.mcm.edu.cn/html_cn/node/a53a84ead7b2e5087dc59954d440219a.html)
- [COMAP MCM/ICM contest matrix](https://www.contest.comap.com/undergraduate/contests/matrix/index.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown analysis with optional shell command and JSON scoring-input guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled scoring script reads contest-ranking JSON and prints Markdown to stdout or writes a Markdown report when an output path is provided.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
