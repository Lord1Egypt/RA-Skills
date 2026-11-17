## Description:

Run Maven commands with full argument passthrough, optionally specifying the working directory, using a Node.js wrapper for safer execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanyongm](https://clawhub.ai/user/yuanyongm)

### License/Terms of Use:


## Use Case:

Developers and build engineers use this skill to have an agent run Maven goals, plugin goals, flags, and Maven information commands against Java projects, with an optional explicit working directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Maven goals, plugins, and POM-defined build steps can execute project-controlled code.

Mitigation: Use trusted repositories and review unusual plugin goals before running them.

Risk: Secrets passed on the command line can be exposed through shell history, logs, or build output.

Mitigation: Avoid passing secrets as Maven command-line arguments and prefer safer secret-handling mechanisms.

Risk: Running the wrapper in an unintended directory can execute the wrong project's build logic.

Mitigation: Prefer explicit --dir paths and confirm the target project before execution.

## Reference(s):

- [Maven Full Runner on ClawHub](https://clawhub.ai/yuanyongm/skills/mvn-full-runner)
- [Artifact README](artifact/README.md)
- [Artifact changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [shell commands, text, guidance]

**Output Format:** [Terminal output and concise Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Executes Maven with full argument passthrough; Maven goals, plugins, and project POMs determine build-side behavior.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
