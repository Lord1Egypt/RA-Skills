## Description:

Provides Go developers with a typed client for calling the Mistral AI REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT

## Use Case:

Go developers use this skill to add and call the go-mistral client from a Go project, including chat completion, embeddings, and other Mistral API operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security analysis was partial: two path-like references in SKILL.md did not resolve to bundled files.

Mitigation: Review the complete skill materials and resolve the missing references before installation; the available scan reported no findings with medium confidence.

Risk: Requests send prompts or files to Mistral AI, and batch or delete operations can have cost or data-removal consequences.

Mitigation: Check what data will be sent and confirm the intended cost or deletion before making those API calls.

Risk: A Mistral API key is used for bearer authentication.

Mitigation: Read the key from an environment variable, keep it out of source control and logs, and avoid printing request headers.

## Reference(s):

- [Setup and reference](references/setup.md)
- [go-mistral package documentation](https://pkg.go.dev/github.com/psyb0t/go-mistral)
- [Project page](https://github.com/psyb0t/go-mistral)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Go and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Integration guidance and examples; the skill describes edits to the current Go project.]

## Skill Version(s):

0.4.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
