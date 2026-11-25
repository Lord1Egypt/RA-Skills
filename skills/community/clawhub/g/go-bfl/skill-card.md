## Description:

Writes Go code with go-bfl (package bfl, github.com/psyb0t/go-bfl), an unofficial generated client for the Black Forest Labs FLUX API. Use when a Go program submits FLUX image or video generation tasks, polls task results, calls the image and video tools, reads credits or manages fine-tunes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to write Go programs that call the FLUX API for image and video generation, check task results and credits, and manage fine-tunes. It guides dependency setup, authentication, request handling, polling, and response validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security analysis was partial because two referenced files were not included in the inspected release files.

Mitigation: Review the missing references or confirm they are not needed before installing.

Risk: API credentials and signed output URLs could be exposed, and generation submissions or fine-tune deletion can affect the user's account.

Mitigation: Keep BFL_API_KEY in the environment, avoid logging credentials or signed URLs, validate polling hosts, and make paid or account-changing calls only when requested.

## Reference(s):

- [Setup and reference](references/setup.md)
- [go-bfl repository homepage](https://github.com/psyb0t/go-bfl)
- [go-bfl package documentation](https://pkg.go.dev/github.com/psyb0t/go-bfl)
- [ClawHub skill page](https://clawhub.ai/psyb0t/skills/go-bfl)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Go and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
