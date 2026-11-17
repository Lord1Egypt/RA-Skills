## Description:

Helps Go developers use go-asyncapi to load and inspect AsyncAPI 3 documents, including local references and merged traits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Go developers use this skill to add go-asyncapi to a project and read servers, channels, operations, messages, and referenced schemas from AsyncAPI 3 YAML or JSON documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Two local path-like references could not be matched to bundled artifacts, leaving part of the scan evidence incomplete.

Mitigation: Review the referenced files and confirm they are expected before installing or relying on the skill.

## Reference(s):

- [go-asyncapi project](https://github.com/psyb0t/go-asyncapi)
- [Setup and reference](references/setup.md)
- [gen-asyncapi](https://github.com/psyb0t/gen-asyncapi)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands]

**Output Format:** [Markdown guidance with Go code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples use the go-asyncapi Go package and AsyncAPI 3 documents.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
