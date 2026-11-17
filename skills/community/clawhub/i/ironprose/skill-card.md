## Description:

Fiction prose analysis - catch weak verbs, repetition, cliches, passive voice, and other craft issues in manuscripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpoehnelt](https://clawhub.ai/user/jpoehnelt)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to run IronProse CLI workflows for JSON prose diagnostics, draft comparison, schema introspection, and diagnostic feedback while reviewing fiction manuscripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs or invokes a mutable external CLI package.

Mitigation: Verify the IronProse package source before installation and pin a known version for repeatable use.

Risk: Manuscript text is sent to a configured remote IronProse API endpoint by default.

Mitigation: Do not submit confidential, unpublished, regulated, or client-owned text unless the endpoint privacy and retention terms are acceptable.

## Reference(s):

- [IronProse CLI homepage](https://github.com/benchcutlogic/ironprose-cli)
- [ClawHub skill page](https://clawhub.ai/jpoehnelt/skills/ironprose)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with shell command examples and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill directs agents to request JSON output from the IronProse CLI for stable downstream parsing.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
