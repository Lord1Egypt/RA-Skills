## Description:

An OSINT sentinel that monitors the public web for email exposure, username footprint, and identity leaks without API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[assix](https://clawhub.ai/user/assix)

### License/Terms of Use:

MIT-0

## Use Case:

Security and privacy practitioners use this skill to check authorized emails, usernames, phone numbers, or search terms for public exposure across OSINT sources and search results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive identifiers such as emails, usernames, phone numbers, and search queries may be sent to external OSINT services or search providers.

Mitigation: Use the skill only for owned or authorized targets, avoid unnecessary sensitive inputs, and disclose external-service use where required.

Risk: Documented shell-style command templates can be unsafe when populated with untrusted input.

Mitigation: Run the skill in an isolated environment, validate inputs before execution, and avoid passing untrusted values through shell commands.

Risk: The skill depends on external OSINT packages and command-line tools that may change behavior over time.

Mitigation: Pin and review dependencies before deployment, then retest the email, username, and search workflows after dependency updates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/assix/skills/identity-monitoring-agent)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [JSON results and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include discovered account registrations, profile URLs, search-result links, or error messages from external OSINT tools.]

## Skill Version(s):

1.0.4 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
