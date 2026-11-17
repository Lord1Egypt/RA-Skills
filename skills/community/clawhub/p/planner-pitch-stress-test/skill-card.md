## Description:

策划案压力测试：在隔离环境中对通过 Pitch Review 的策划案执行四轮对抗式攻击，验证不可替代性。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangliujiao-tal](https://clawhub.ai/user/huangliujiao-tal)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, development teams, and pitch reviewers use this skill after Pitch Review to run an isolated, adversarial four-part stress test of a series pitch before downstream development.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill applies strict reject and redo criteria that can block downstream development.

Mitigation: Use it as a post-Pitch Review gate and review the concrete notes and mandatory rewrites before deciding whether to reject or resubmit.

Risk: The skill asks for an isolated review session, so missing pitch context can lead to overly narrow critiques.

Mitigation: Provide the passed Pitch Review draft and relevant theme, character, market, and series-engine context before running the stress test.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON object with scored attack notes and mandatory rewrite items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Four attack sections with 1-5 scores, notes, optional flags, a verdict, and combined mandatory rewrites.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
