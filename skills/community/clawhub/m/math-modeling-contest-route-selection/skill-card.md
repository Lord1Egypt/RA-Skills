## Description: <br>
Select superior mathematical modeling contest problems and modeling-solution routes for CUMCM A/B/C, MCM, ICM, and similar contests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[y3519712124-ui](https://clawhub.ai/user/y3519712124-ui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External contest participants, coaches, and modeling teams use this skill to compare contest topics, select feasible modeling routes, test alternatives, and plan validation and fallback paths for stronger papers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Topic and route recommendations can be misleading when contest statements, team skills, data availability, or validation evidence are incomplete. <br>
Mitigation: Provide full problem statements and team constraints, review assumptions and scoring evidence, and use the skill's baseline, refutation, and fallback checks before relying on a recommendation. <br>
Risk: The bundled scoring script depends on user-provided JSON and selected output paths. <br>
Mitigation: Review scoring JSON before execution and choose output paths deliberately; the security scan found no credential requirement, hidden data access, exfiltration, or unsafe automatic actions. <br>


## Reference(s): <br>
- [Award Method Distillation](references/award-method-distillation.md) <br>
- [Award-Style Question Decomposition](references/award-question-decomposition.md) <br>
- [Award Route Pattern Library](references/award-route-pattern-library.md) <br>
- [Contest Archives](references/contest-archives.md) <br>
- [Engineering Feasibility](references/engineering-feasibility.md) <br>
- [Method Map](references/method-map.md) <br>
- [Paper Scoring Framework](references/paper-scoring-framework.md) <br>
- [Problem Taxonomy](references/problem-taxonomy.md) <br>
- [Refutation and Model Choice](references/refutation-and-model-choice.md) <br>
- [Selection Rubric](references/selection-rubric.md) <br>
- [CUMCM Official Site](https://www.mcm.edu.cn/) <br>
- [CUMCM Historical Problem Archive](https://www.mcm.edu.cn/html_cn/node/a53a84ead7b2e5087dc59954d440219a.html) <br>
- [COMAP MCM/ICM Contest Matrix](https://www.contest.comap.com/undergraduate/contests/matrix/index.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with structured comparisons, JSON scoring data, and optional shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use a local scoring script when valid scoring JSON is provided; recommendations should be reviewed against the full contest statements and team constraints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
