## Description:

Use this skill when the user wants to install, configure, or troubleshoot the GNews binary from GitHub and fetch top headlines from GNews by country, category, and max article count.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parinll](https://clawhub.ai/user/parinll)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and CLI users use this skill to install or build the GNews Go client, configure GNEWS_API_KEY, run headline queries, and troubleshoot API key, permission, and network issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides users to build and run unpinned code from GitHub.

Mitigation: Review the upstream repository before installation and prefer a pinned release or commit with checksum or signature verification.

Risk: The troubleshooting guidance includes a command that can expose GNEWS_API_KEY.

Mitigation: Use a non-printing presence check for the environment variable and rotate the API key if it was printed or shared.

Risk: Optional global installation uses elevated privileges.

Mitigation: Avoid sudo global installation unless needed and inspect the binary source before installing it into a shared PATH.

## Reference(s):

- [GNews CLI upstream repository](https://github.com/ParinLL/gnewsapi-go-client)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with bash command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GNEWS_API_KEY and Go when following install or build guidance.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
