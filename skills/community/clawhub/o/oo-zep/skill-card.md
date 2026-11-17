## Description:

Use Zep to manage user profiles, conversation threads, messages, and graph context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to retrieve Zep project, user, thread, message, and graph context, and to create or update Zep records. Review proposed changes and confirm write or deletion actions before they run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation fallback executes unverified remote code and may make broader agent changes than users expect.

Mitigation: Install the CLI separately from a verified source, review the setup steps, and consider disabling automatic skill synchronization with OO_SKILLS_SYNC_DISABLED.

Risk: Sensitive Zep requests pass through OOMOL, and write or deletion actions change stored data.

Mitigation: Consider the sensitivity of requests sent through OOMOL, review the exact payload and effect, and require confirmation before writes or deletions.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Zep](https://www.getzep.com)
- [Zep SDK Reference](https://help.getzep.com/sdk-reference)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes confirmation guidance for state-changing actions.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
