## Description:

Anymail Finder (anymailfinder.com). Use this skill for ANY Anymail Finder request — searching and reading data. Whenever a task involves Anymail Finder, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using Anymail Finder can search for verified company or person work email addresses, check email deliverability, and view their account and remaining credits through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup can execute remote code, and startup synchronization can make persistent changes to other agent skills.

Mitigation: Review and verify the CLI installation before using fallback setup commands. Set OO_SKILLS_SYNC_DISABLED=1 to disable startup synchronization.

Risk: Lookup details are shared with OOMOL and Anymail Finder, and lookups may use account credits.

Mitigation: Submit only lookup details you authorize sharing and check the available credits before using the service.

## Reference(s):

- [Anymail Finder](https://anymailfinder.com/)
- [Anymail Finder API documentation](https://anymailfinder.com/email-finder-api/docs)
- [OO CLI commands and synchronization controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Text with shell command examples and JSON connector results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected lookup or account action.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
