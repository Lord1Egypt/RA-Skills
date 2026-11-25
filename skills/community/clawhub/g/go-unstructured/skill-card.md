## Description:

Unofficial Go clients for the Unstructured Platform and Partition APIs, generated with oapi-codegen. Package unstructured covers sources, destinations, workflows, jobs, templates, notifications and usage; subpackage partition handles multipart document extraction. Use when Go code needs Unstructured API calls or already imports github.com/psyb0t/go-unstructured.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT

## Use Case:

Go developers use this skill to integrate applications with Unstructured Platform APIs and partition documents into elements through the unofficial typed Go clients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected documents are sent to Unstructured when using document upload or partition workflows.

Mitigation: Review the document and share it only when the user has authorized sending it to the service.

Risk: The available security scan is incomplete because three path-like references could not be resolved.

Mitigation: Review the skill and the unresolved references before installing or using it.

## Reference(s):

- [Setup and API reference](artifact/references/setup.md)
- [Source repository](https://github.com/psyb0t/go-unstructured)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-unstructured)
- [ClawHub skill page](https://clawhub.ai/psyb0t/skills/go-unstructured)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Go and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.3.8 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
