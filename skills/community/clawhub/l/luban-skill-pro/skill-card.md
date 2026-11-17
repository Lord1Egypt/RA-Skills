## Description:

鲁班.Skill is an industrial agent-skill optimizer that evaluates, improves, validates, audits, hardens, and streamlines agent skills through repeatable review workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ebandao777-oss](https://clawhub.ai/user/ebandao777-oss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to assess and improve agent skill quality with structured scoring, test prompts, review checkpoints, regression checks, and optimization logs. It is intended for skill-maintenance workflows such as evaluating all skills, optimizing a specific skill, checking skill health, updating references, and reviewing optimization history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad repository edits and Git writes can alter skill behavior or history.

Mitigation: Use the skill only in a sandboxed skill repository and require explicit approval of exact files and diffs before writes to Git, references, tests.yaml, or generated prompt files.

Risk: Scheduled maintenance, CASCADE web updates, and automatic MUSE test persistence can introduce ongoing changes without clear review.

Mitigation: Disable scheduled runs, CASCADE web updates, and automatic MUSE test persistence until the release is reviewed and governance controls are in place.

Risk: The security scan verdict is suspicious because approval boundaries are not consistently clear.

Mitigation: Review before installing and scan the skill before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ebandao777-oss/skills/luban-skill-pro)
- [README](artifact/README.md)
- [Quickstart](artifact/QUICKSTART.md)
- [Agent智能体技能进化方法论](artifact/references/SA-DM.md)
- [baseline-skill](artifact/references/baseline-skill.md)
- [EvoSkill](https://arxiv.org/abs/2603.02766)
- [SkillOps](https://arxiv.org/abs/2605.13716)
- [CASCADE](https://arxiv.org/abs/2512.23880)
- [Skill Distill](https://arxiv.org/abs/2604.01608)
- [HASP](https://arxiv.org/abs/2605.17734)
- [MUSE-Autoskill](https://arxiv.org/abs/2605.27366)
- [SkillLens](https://arxiv.org/abs/2605.23899)
- [SkillOpt](https://arxiv.org/abs/2605.23904)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, scoring tables, proposed diffs, inline shell commands, and file artifacts such as results.tsv, test-prompts.json, tests.yaml, and rejected_edits.md]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or perform skill-file and Git changes when the workflow reaches confirmed edit stages; read-only scans produce reports without edits.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
