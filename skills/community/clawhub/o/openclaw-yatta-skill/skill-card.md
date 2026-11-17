## Description:

Yatta! - Task & Capacity Management helps an agent manage Yatta tasks, projects, contexts, calendar and capacity views, analytics, and follow-ups through authenticated API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrisagiddings](https://clawhub.ai/user/chrisagiddings)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to operate a Yatta account from an agent, including task organization, project tracking, delegation follow-up, calendar subscriptions, capacity planning, and productivity reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a full-access Yatta API key and can perform account-changing operations.

Mitigation: Require explicit user confirmation for create, update, batch, archive, calendar sync, and comment-delete actions before running commands.

Risk: A configured endpoint could expose the API key if it is not the intended Yatta API endpoint.

Mitigation: Use only a verified Yatta API endpoint, prefer the documented Supabase default, and rotate the API key if endpoint configuration may have been exposed.

Risk: Unsafe authenticated API snippets can cause injection or unintended data changes if copied without input-safe JSON and URL handling.

Mitigation: Use jq-built JSON payloads, URL-encoded identifiers, and the provided safe API wrapper patterns before executing API examples.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/chrisagiddings/skills/openclaw-yatta-skill)
- [Yatta! Product Site](https://yattadone.com)
- [Yatta! API Documentation](https://yattadone.com/docs/api)
- [API Reference](API-REFERENCE.md)
- [Security Guidance](SECURITY.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, curl, jq, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires YATTA_API_KEY and optionally YATTA_API_URL; commands may create, update, archive, or delete Yatta account data.]

## Skill Version(s):

0.2.2 (source: package.json, CHANGELOG, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
