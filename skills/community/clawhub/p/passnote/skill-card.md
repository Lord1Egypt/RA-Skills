## Description:

Create and manage disposable memos using PassNote. Share secure, auto-destructing notes with others.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shiweifu](https://clawhub.ai/user/shiweifu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill through OpenClaw to create temporary PassNote memos and return the generated viewing URL and passcode to the requester.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends memo content and an API bearer token to the configured PassNote endpoint.

Mitigation: Configure PASSNOTE_API_URL only for a trusted PassNote server, prefer HTTPS, and restrict the API token scope where possible.

Risk: The security review reports weak endpoint safety and incomplete disclosure for secret-handling behavior.

Mitigation: Review the skill before installing, avoid high-value passwords or regulated data unless you control the server and token scope, and rotate the token if it may have been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shiweifu/skills/passnote)
- [OpenClaw PassNote Skill README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown text with shell command examples and generated PassNote URL and passcode output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PASSNOTE_API_URL and PASSNOTE_API_TOKEN; default memo expiration is 24 hours and can be configured up to 48 hours.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
