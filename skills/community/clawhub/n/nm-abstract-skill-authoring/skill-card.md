## Description: <br>
Guide creating Claude Code skills with TDD and persuasion principles. Use for new skill development <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to design, validate, and refine Claude Code skills using test-driven development, progressive disclosure, and anti-rationalization patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persuasion framing may make generated skill guidance sound more mandatory than the user's actual policy requires. <br>
Mitigation: Review the resulting skill text for appropriate scope, explicit exceptions, and alignment with the user's stated requirements. <br>
Risk: Deployment and rollback examples can affect real repositories if copied without checking local context. <br>
Mitigation: Confirm the repository, branch, paths, and target skill name before running any deployment or rollback command. <br>
Risk: Broad activation triggers may cause the skill to load for unrelated skill-writing or validation tasks. <br>
Mitigation: Review and test activation triggers in the target environment before enabling automatic skill loading. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-abstract-skill-authoring) <br>
- [Publisher profile](https://clawhub.ai/user/athola) <br>
- [Metadata homepage](https://github.com/athola/claude-night-market/tree/master/plugins/abstract) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with examples, checklists, and inline shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Focuses on skill-authoring process guidance; examples should be reviewed before use in a live repository.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence and target metadata; artifact frontmatter says 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
