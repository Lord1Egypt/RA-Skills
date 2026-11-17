## Description:

LinkedIn outreach automation for searching leads, sending connection requests, sending follow-up messages, and generating outreach reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[limoxt](https://clawhub.ai/user/limoxt)

### License/Terms of Use:

MIT

## Use Case:

External users and sales operators use this skill to automate LinkedIn prospect discovery, connection outreach, follow-up messaging, and CSV or JSON reporting. Review all recipients, message content, and LinkedIn account-use constraints before sending outreach.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles LinkedIn credentials and stores reusable login session state locally.

Mitigation: Install only in an environment where local session cookies are acceptable, prefer a dedicated or hardened local user profile, restrict file permissions, and remove stored session data when no longer needed.

Risk: The skill can send real connection requests and follow-up messages in bulk.

Mitigation: Manually verify every recipient and message before running send commands, use dry-run behavior where available, and add explicit send confirmations before production use.

Risk: The security verdict is suspicious because safeguards around stored account state and bulk outreach are limited.

Mitigation: Follow the server-provided security guidance: update dependencies, add owner-only permissions, implement deletion or logout support, sanitize CSV output, and review the skill carefully before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/limoxt/skills/linkedin-outreach)
- [Publisher profile](https://clawhub.ai/user/limoxt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code, Files]

**Output Format:** [Markdown guidance, CLI commands, local JSON state, and CSV or JSON reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local browser automation and writes session, usage, contact, pending outreach, and report data under the user's local configuration or chosen output path.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact frontmatter and package.json list 1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
