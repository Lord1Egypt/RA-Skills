## Description:

Skill architect and builder. Designs, builds, and validates complete Agent Skill packages through a mandatory eight-phase pipeline. Default output is the finished installable package. Not for skill evaluation (use skilllab) or variant proposals (use ocas-mentor).

This skill is ready for commercial/non-commercial use.

## Publisher:

[indigokarasu](https://clawhub.ai/user/indigokarasu)

### License/Terms of Use:

MIT

## Use Case:

Developers and skill-library maintainers use Forge to design, build, repair, consolidate, and validate Agent Skill packages through a required pipeline. It is used when the desired output is a complete installable skill package, validation report, journal entry, or synchronization guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Forge can manage skills, repositories, journals, and OCAS dispatch state, so misuse or incorrect commands can mutate local skill-library state.

Mitigation: Install only from a trusted publisher and review sync, consolidate, closure, and fix operations before allowing them to run.

Risk: The security scan reports under-disclosed credential-authoring guidance and self-update behavior.

Mitigation: Review or disable self-update cron behavior before use and inspect generated skill reference files for credential access.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/indigokarasu/skills/ocas-forge)
- [SKILL.md](SKILL.md)
- [README.md](README.md)
- [Design Pipeline](references/design_pipeline.md)
- [Authoring Rules](references/authoring_rules.md)
- [Builder Workflows](references/builder_workflows.md)
- [Dispatch Pipeline Guide](references/dispatch-pipeline-guide.md)
- [Schemas](references/schemas.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code, shell command, and configuration snippets; may also produce installable skill-package files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include package files, validation findings, journals, and synchronization instructions.]

## Skill Version(s):

2.3.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
