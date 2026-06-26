## Description: <br>
Forge creates, reviews, repairs, and validates complete Agent Skill packages through a mandatory six-phase pipeline that outputs finished installable skill files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[indigokarasu](https://clawhub.ai/user/indigokarasu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use Forge to design, build, critique, repair, and validate Agent Skill packages. It is intended for complete skill package production rather than one-off plans, skill evaluation, or non-skill artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Forge can create or change skill packages, process intake files, and write run journals. <br>
Mitigation: Review generated or repaired skill files before enabling them, and restrict who or what can write to the Mentor intake path. <br>
Risk: Forge registers background jobs, including a daily self-update that may replace installed files from GitHub. <br>
Mitigation: Review scheduled jobs before installation and disable the daily self-update unless automatic replacement is acceptable. <br>


## Reference(s): <br>
- [Forge ClawHub release](https://clawhub.ai/indigokarasu/ocas-forge) <br>
- [Authoring Rules](references/authoring_rules.md) <br>
- [Package Patterns](references/package_patterns.md) <br>
- [Examples](references/examples.md) <br>
- [Journal](references/journal.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown instructions plus complete skill package files and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include installable skill package contents, validation findings, repair changes, journals, and local configuration records.] <br>

## Skill Version(s): <br>
2.3.0 (source: server release evidence, skill.json, README changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
