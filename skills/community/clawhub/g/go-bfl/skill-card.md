## Description:

Writes Go code with go-bfl (package bfl, github.com/psyb0t/go-bfl), an unofficial generated client for the Black Forest Labs FLUX API. Use when a Go program submits FLUX image or video generation tasks, polls task results, calls the image and video tools, reads credits or manages fine-tunes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to write Go programs that call the unofficial go-bfl client for FLUX image and video generation, task polling, credits, and fine-tune management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API key or task data could be exposed if credentials are logged or sent to an untrusted polling URL.

Mitigation: Read BFL_API_KEY from the environment, keep it private, and validate HTTPS and an approved provider host before following polling URLs.

Risk: Image or video submissions spend credits, and deleting a fine-tune changes account state.

Mitigation: Submit paid tasks and delete fine-tunes only when requested; avoid blindly retrying a paid submission after an uncertain result.

## Reference(s):

- [Setup and reference](artifact/references/setup.md)
- [go-bfl package documentation](https://pkg.go.dev/github.com/psyb0t/go-bfl)
- [ClawHub skill release](https://clawhub.ai/psyb0t/skills/go-bfl)

## Skill Output:

**Output Type(s):** [Go code, Shell commands, Configuration guidance, Technical guidance]

**Output Format:** [Markdown with Go and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples and guidance depend on the requested FLUX operation and user-supplied prompts or configuration.]

## Skill Version(s):

0.1.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
