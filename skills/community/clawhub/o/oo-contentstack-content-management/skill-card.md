## Description:

Use this skill to read, create, and update Contentstack content through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to inspect Contentstack content types and entries, list content, and create or update entries through the connected Contentstack account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI installation or the hosted connector implementation may involve code that has not been verified.

Mitigation: Review the installer and install a vetted CLI version before use; treat the hosted connector implementation as unverified.

Risk: Startup synchronization can introduce additional agent skills without explaining the changes.

Mitigation: Review synchronization changes or set OO_SKILLS_SYNC_DISABLED=1 to disable startup synchronization.

Risk: Create and update actions can change Contentstack content.

Mitigation: Connect only the needed Contentstack access, inspect the live action schema, and review and confirm each write payload and its effect before running it.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/oomol/skills/oo-contentstack-content-management)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [Contentstack Content Management API documentation](https://www.contentstack.com/docs/developers/apis/content-management-api)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, JSON, Guidance]

**Output Format:** [CLI commands with JSON payloads and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action inputs should follow the live connector schema.]

## Skill Version(s):

1.0.4 (source: release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
