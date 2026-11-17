## Description:

Helps Hermes users give each AI assistant an isolated, persistent, headless browser profile and check for browser conflicts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lingyu9495-source](https://clawhub.ai/user/lingyu9495-source)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other Hermes users can set up separate browser sessions for multiple AI assistants, preserve each session's login state, and audit whether those browsers are running without visible windows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent logged-in browser profiles are exposed through unauthenticated local debugging ports.

Mitigation: Install only on a trusted single-user machine, review assigned ports, and avoid storing high-value accounts in these profiles.

Risk: Scheduled apply or audit tasks can repeatedly control local browser processes.

Mitigation: Enable scheduled tasks only if recurring local process control is acceptable.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/lingyu9495-source/skills/hermes-profile-browser-isolation)
- [Design notes](references/design-notes.md)
- [Platform notes](references/platform-notes.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Audit reports]

**Output Format:** [Markdown guidance and plain-text or JSON audit results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Describes per-profile browser setup and reports instance status and visible-window checks.]

## Skill Version(s):

1.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
