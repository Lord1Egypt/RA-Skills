## Description:

Command-line JSON processor. Extract, filter, transform JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill as a concise jq reference for extracting, filtering, transforming, and safely handling JSON on the command line.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill includes unsafe command and secret-handling examples that need review before use.

Mitigation: Review jq shell examples before deployment, especially examples that combine jq output with shell evaluation or network-transmitting commands.

Risk: jq output can contain shell metacharacters or secrets that become unsafe when copied directly into shell or network pipelines.

Mitigation: Avoid inserting jq output directly into sh -c source, and do not copy examples that extract secrets from JSON and send them with curl or similar tools.

## Reference(s):

- [jq downloads](https://jqlang.org/download/)
- [Faberlens safety evaluation](https://faberlens.ai)

## Skill Output:

**Output Type(s):** [guidance, shell commands]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces jq usage guidance and command examples for an agent; it does not execute commands.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
