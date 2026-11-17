## Description:

URLhaus (urlhaus.abuse.ch). Use this skill for ANY URLhaus request — searching and reading data. Whenever a task involves URLhaus, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security analysts can use the skill to check whether a URL is listed by URLhaus as a malware distribution site and review its threat details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI installation may execute unverified remote code or make broader changes to the agent environment.

Mitigation: Review installation separately, prefer a verified pinned release, and review automatic skill synchronization before first use; consult the command reference for OO_SKILLS_SYNC_DISABLED.

Risk: Submitted URLs may be shared with OOMOL and URLhaus, and the remote installer payload and exact installed version are unverified.

Mitigation: Submit only URLs you are comfortable sharing, and verify the installer and installed version before use.

## Reference(s):

- [URLhaus](https://urlhaus.abuse.ch)
- [URLhaus API documentation](https://urlhaus-api.abuse.ch/)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON results with concise natural-language guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include threat status, blacklist status, tags, payload details, or a not-found result.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
