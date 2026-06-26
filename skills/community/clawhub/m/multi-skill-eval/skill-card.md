## Description: <br>
Integrated OpenClaw skill evaluation toolkit that combines static analysis, a 25-criterion rubric, and agent-orchestrated benchmark workflows to evaluate, compare, audit, and improve skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangzairong](https://clawhub.ai/user/wangzairong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to assess OpenClaw skills before publishing or revising them. It supports quick static checks, detailed rubric scoring, benchmark comparison, and evaluation report generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Evaluator scripts run against local skill directories and may inspect or process sensitive skill contents. <br>
Mitigation: Run the toolkit only on skill directories you trust or inside a sandbox, and avoid supplying unnecessary credentials or private data. <br>
Risk: Benchmark workflows can involve broad agent execution against target skills. <br>
Mitigation: Use benchmark mode only with trusted or sandboxed target skills and review generated outputs before reuse. <br>
Risk: Generated leaderboard HTML may be unsafe when built from untrusted skill cards. <br>
Mitigation: Avoid opening generated leaderboard HTML from untrusted inputs until the HTML escaping issue identified by security evidence is fixed. <br>
Risk: Generated skill rewrites or improvement suggestions may introduce inaccurate or risky guidance. <br>
Mitigation: Review and scan any generated rewrite before making it active. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/wangzairong/multi-skill-eval) <br>
- [Evaluation rubric](references/rubric.md) <br>
- [Evaluation template](assets/EVAL-TEMPLATE.md) <br>
- [SkillLens security scanner](https://www.npmjs.com/package/skilllens) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown reports, JSON grading data, leaderboard HTML, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Benchmark mode depends on trusted or sandboxed target skills and agent execution.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
