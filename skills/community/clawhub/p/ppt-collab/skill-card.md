## Description:

Use when working in the PPTAgent or BotSlide repository to add features, fix bugs, or adjust slide generation, editing, export, prompt rules, project versioning, or preview behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrguanglei](https://clawhub.ai/user/mrguanglei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill while working inside PPTAgent or BotSlide repositories to navigate slide generation, editing, preview, export, versioning, and validation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Following validation steps may install dependencies or run local services in a development environment.

Mitigation: Review dependency manifests and lockfiles first, and run installs in a contained development environment without unrelated secrets.

Risk: Slide layout, preview, or export changes can break fixed 1280x720 rendering assumptions or PPTX export fidelity.

Mitigation: Check generated slide output against the fixed canvas rules and run a PPTX export smoke test when export behavior changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mrguanglei/skills/ppt-collab)
- [项目地图](references/project-map.md)
- [幻灯片规则](references/slide-rules.md)
- [验证方式](references/validation.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown prose with inline code, commands, and file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes task-scoped validation guidance and explicit verification gaps when complete validation is not possible.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
