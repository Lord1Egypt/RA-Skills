## Description:

Multi-Skill-Eval helps agents evaluate, audit, benchmark, compare, and improve OpenClaw skills through static analysis, rubric scoring, and autonomous benchmark workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangzairong](https://clawhub.ai/user/wangzairong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to assess OpenClaw skills before release or revision. It supports quick static checks, detailed rubric scoring, benchmark comparison, and report generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit workflow is under-scoped and may produce incomplete or misleading evaluation conclusions.

Mitigation: Review generated findings before acting on them, and treat benchmark or rubric output as decision support rather than an automatic release gate.

Risk: Skills submitted for evaluation may be exposed to the selected model or provider during benchmark workflows.

Mitigation: Run the skill only on artifacts that are acceptable to share with the selected model/provider, and avoid submitting sensitive or private skill content unless the provider arrangement permits it.

Risk: Generated leaderboard HTML can include unsafe unescaped content from untrusted cards.

Mitigation: Do not open or publish generated leaderboards from untrusted card inputs until HTML escaping is fixed or the output has been reviewed in an isolated environment.

Risk: Third-party scanner execution can introduce supply-chain and execution-environment risk.

Mitigation: Run scanners in an isolated environment with pinned versions and review the scanner command before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangzairong/skills/multi-skill-eval)
- [Evaluation rubric](references/rubric.md)
- [Evaluation template](assets/EVAL-TEMPLATE.md)
- [SkillLens package](https://www.npmjs.com/package/skilllens)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON grading summaries, Markdown skill cards, and HTML leaderboard files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create report files such as EVAL.md, grading.json, benchmark summaries, skill cards, and leaderboard HTML when the user runs the bundled scripts.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
