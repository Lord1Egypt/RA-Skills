## Description:

Create a Linkfuse affiliate short link from any URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oliverw](https://clawhub.ai/user/oliverw)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to create or recycle Linkfuse affiliate short links from provided URLs through the Linkfuse API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A returned short URL could make the documented clipboard shell command unsafe if the URL contains shell syntax.

Mitigation: Avoid running the clipboard command as written; copy the displayed short URL manually or use a shell-safe clipboard helper that validates the URL first.

Risk: The skill submits destination URLs to Linkfuse and requires a bearer token.

Mitigation: Use this skill only when Linkfuse is trusted with the submitted URLs and the LINKFUSE_TOKEN can be stored and handled securely.

## Reference(s):

- [Linkfuse](https://www.linkfuse.net)
- [Linkfuse external token page](https://app.linkfuse.net/user/external-token)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline shell commands and Linkfuse short-link result text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+, network access, and a LINKFUSE_TOKEN environment variable.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
