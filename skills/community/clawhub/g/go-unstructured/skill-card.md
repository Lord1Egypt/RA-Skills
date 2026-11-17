## Description:

Unofficial Go clients for the Unstructured Platform and Partition APIs, generated with oapi-codegen. Package unstructured covers sources, destinations, workflows, jobs, templates, notifications and usage; subpackage partition handles multipart document extraction. Use when Go code needs Unstructured API calls or already imports github.com/psyb0t/go-unstructured.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Go developers use this skill to build code that calls Unstructured Platform operations or partitions documents through the Unstructured API clients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploading a document sends its contents to Unstructured, which may expose sensitive information.

Mitigation: Before uploading, check the document's sensitivity and confirm it is appropriate to send to Unstructured.

## Reference(s):

- [Setup and reference](references/setup.md)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-unstructured)
- [Project homepage](https://github.com/psyb0t/go-unstructured)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Go code and Markdown guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples and setup guidance for Platform and Partition API clients]

## Skill Version(s):

0.3.7 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
