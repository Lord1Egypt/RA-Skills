## Description: <br>
设计并产出可发布的 Agent Skill（L4生产级）。用于从0到1创建技能、重构现有技能、做安全评审、建立评估与发布流程。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reffwu](https://clawhub.ai/user/reffwu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and teams use this skill to design, refactor, review, evaluate, and package production-grade Agent Skills with templates, release checks, and evaluation cases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrases may activate the skill for generic skill-related requests. <br>
Mitigation: Install only when a skill-focused assistant is desired and review whether the current request actually needs skill creation, review, or release guidance. <br>
Risk: The included Node scripts can scaffold or score local skill directories in the active workspace. <br>
Mitigation: Run included scripts only in a workspace intended for modification, and treat scoring output as a checklist signal rather than a security certification. <br>


## Reference(s): <br>
- [L4 Production Standard](references/l4-standard.md) <br>
- [Onboarding Zero to One](references/onboarding-zero-to-one.md) <br>
- [Behavioral Testing](references/behavioral-testing.md) <br>
- [CSO Guide](references/cso-guide.md) <br>
- [Benchmark vs Official](references/benchmark-vs-official.md) <br>
- [Release Checklist](assets/checklists/release-checklist.md) <br>
- [Evaluation Cases](assets/evals/eval-cases.md) <br>
- [Skill Blueprint Template](assets/templates/skill-blueprint.md) <br>
- [First Skill Exercise](assets/templates/first-skill-exercise.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/reffwu/l4-skill-forge) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with file plans, templates, checklists, evaluation cases, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify skill package files when the agent environment has filesystem access and the user confirms high-impact actions.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
