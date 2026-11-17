## Description:

Connects to Clearout to verify email addresses and check available credits and verification limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use the skill to check email verification categories and review Clearout credits through an existing OOMOL connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented automatic setup runs an unverified remote CLI installer, and the security review says the resulting skill synchronization changes are not fully disclosed.

Mitigation: Review and verify the CLI installation before running it, and disable skill synchronization if it is not wanted using OO_SKILLS_SYNC_DISABLED.

Risk: Email addresses submitted for verification are processed by OOMOL and Clearout.

Mitigation: Submit only email addresses you intend those services to process.

## Reference(s):

- [Clearout](https://clearout.io)
- [Clearout API documentation](https://docs.clearout.io/developers/api/overview)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands]

**Output Format:** [oo CLI commands and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Email verification results and Clearout credit information; access depends on an existing OOMOL connection and available account credits.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
