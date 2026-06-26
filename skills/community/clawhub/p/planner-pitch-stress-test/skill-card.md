## Description: <br>
策划案压力测试：在隔离环境中对通过 Pitch Review 的策划案执行四轮对抗式攻击，验证不可替代性。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangliujiao-tal](https://clawhub.ai/user/huangliujiao-tal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creative development teams and agents use this skill after Pitch Review to stress-test a pitch before downstream development. It evaluates market appeal, story engine durability, character necessity, and emotional engagement, then returns PASS, CONDITIONAL, or REJECT with required rewrite targets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may block downstream creative work because it applies strict review gates to pitches. <br>
Mitigation: Treat REJECT and CONDITIONAL outcomes as review findings for human creative leads to evaluate before halting or restarting work. <br>
Risk: Pitch review output may be incorrect or overly harsh if the input pitch lacks context. <br>
Mitigation: Provide the full Pitch Review pass output and require notes to cite specific issues before acting on mandatory rewrites. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huangliujiao-tal/planner-pitch-stress-test) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/huangliujiao-tal) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, json, guidance] <br>
**Output Format:** [JSON stress-test report with scores, notes, verdict, and mandatory rewrite items] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill is intentionally strict and may block downstream creative work until pitch weaknesses are addressed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
