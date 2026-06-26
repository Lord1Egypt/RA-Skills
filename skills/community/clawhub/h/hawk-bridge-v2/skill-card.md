## Description: <br>
Automates repository inspection and iterative improvement by analyzing projects from user, product, project, and technical perspectives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[relunctance](https://clawhub.ai/user/relunctance) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use Workspace to inspect repositories, identify improvement opportunities, and review or apply proposed changes through dry-run, semi-auto, or configured automation modes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify, commit, push, or post to repositories. <br>
Mitigation: Start with dry-run or semi-auto mode and require human review before enabling full automation on important repositories. <br>
Risk: Code, repository context, and local persona memory may be sent to a configured LLM provider. <br>
Mitigation: Use approved LLM providers, avoid sensitive repositories unless authorized, and tightly control or disable available API tokens. <br>
Risk: Persistent scheduled jobs can continue operating after initial setup. <br>
Mitigation: Review configured repositories and schedules regularly, and avoid scheduling full-auto operation on sensitive repositories. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/relunctance/hawk-bridge-v2) <br>
- [README](artifact/README.md) <br>
- [Quality Gates](artifact/references/QUALITY-GATES.md) <br>
- [Risk Classification](artifact/references/RISK-CLASSIFICATION.md) <br>
- [Notification Template](artifact/references/NOTIFICATION-TEMPLATE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, CLI output, JSON configuration, and repository changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create scheduled jobs, persistent learning records, commits, pushes, or repository comments when configured.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
