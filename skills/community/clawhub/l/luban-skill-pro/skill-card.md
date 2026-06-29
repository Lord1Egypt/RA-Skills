## Description: <br>
鲁班.Skill helps an agent evaluate, optimize, test, and maintain other agent skills through scoring rubrics, checkpoints, rollback guidance, and maintenance reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ebandao777-oss](https://clawhub.ai/user/ebandao777-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent maintainers use this skill to review skill quality, generate test prompts, propose targeted improvements, record score changes, and keep skill repositories healthy over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct broad repository-scale inspection, editing, testing, and maintenance of many skills. <br>
Mitigation: Use it only in a version-controlled workspace, scope each run to explicit target skills, review diffs before accepting edits, and require user confirmation before every write. <br>
Risk: Automatic or periodic maintenance, web refresh, child-agent testing, and bulk optimization can change behavior beyond the immediate user request. <br>
Mitigation: Treat these flows as opt-in review actions and disable or decline them unless the user explicitly requests that mode. <br>
Risk: Repair and testing workflows may expose confidential prompts, skill content, or other sensitive workspace context. <br>
Mitigation: Avoid providing secrets or confidential prompts during repair and testing, and sanitize examples before using generated test prompts or child-agent evaluations. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/ebandao777-oss/luban-skill-pro) <br>
- [README](artifact/README.md) <br>
- [Quickstart](artifact/QUICKSTART.md) <br>
- [Scenario-Adaptive Dual-Mode Architecture reference](artifact/references/SA-DM.md) <br>
- [Baseline skill reference](artifact/references/baseline-skill.md) <br>
- [EvoSkill paper](https://arxiv.org/abs/2603.02766) <br>
- [SkillOps paper](https://arxiv.org/abs/2605.13716) <br>
- [CASCADE paper](https://arxiv.org/abs/2512.23880) <br>
- [Skill Distill paper](https://arxiv.org/abs/2604.01608) <br>
- [HASP paper](https://arxiv.org/abs/2605.17734) <br>
- [MUSE-Autoskill paper](https://arxiv.org/abs/2605.27366) <br>
- [SkillLens paper](https://arxiv.org/abs/2605.23899) <br>
- [SkillOpt paper](https://arxiv.org/abs/2605.23904) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, score tables, proposed edits, test prompts, patch guidance, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce repository-maintenance artifacts such as results.tsv, test-prompts.json, tests.yaml, rejected_edits.md, backup files, and git branch or commit guidance when the user confirms write actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
