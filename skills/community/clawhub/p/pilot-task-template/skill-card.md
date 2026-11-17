## Description:

Reusable task templates with placeholder substitution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to define reusable, parameterized task templates and submit standardized task descriptions through Pilot Protocol tooling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe placeholder substitution can produce unintended shell or task content when template variables are not trusted.

Mitigation: Use trusted template names and trusted variable values, validate placeholders strictly, and prefer a safer template engine for production use.

Risk: Template contents and substituted prompts may be sent to an external Pilot agent.

Mitigation: Do not include secrets or sensitive local content unless the target Pilot agent is authorized to receive that information.

Risk: Path-concatenation patterns for loading templates can read unintended files when template names are untrusted.

Mitigation: Restrict template names to an approved allowlist or canonicalize paths inside the expected template directory before reading files.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-task-template)
- [ClawHub publisher profile](https://clawhub.ai/user/teoslayer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces reusable task template patterns, placeholder substitution examples, and Pilot task submission commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
