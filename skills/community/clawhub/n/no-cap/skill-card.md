## Description:

Automatically ingest X/Twitter bookmarks, filter noise, and extract actionable signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zephyr2800](https://clawhub.ai/user/zephyr2800)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and individual users use No Cap to process X/Twitter bookmarks into structured signal reports, action items, project-relevant notes, and optional email digests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for live X session cookies and browser or Keychain access.

Mitigation: Use only if the user accepts that credential access; prefer scoped OAuth or secure secret prompting when available.

Risk: The skill stores session credentials locally.

Mitigation: Keep the configuration file owner-only readable and avoid sharing generated config or signal directories.

Risk: The reviewed artifact references an external CLI implementation that was not included in the artifact.

Mitigation: Review the installed CLI source and commands before running bookmark fetch, cookie extraction, or email-send operations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zephyr2800/skills/no-cap)
- [X](https://x.com)
- [Resend](https://resend.com)

## Skill Output:

**Output Type(s):** [Markdown, HTML, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown session and master files, optional HTML email digest, inline shell commands, and JSON configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes outputs to a user-configured signal directory and may generate an optional email digest.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
