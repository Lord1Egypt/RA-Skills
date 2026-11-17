## Description:

Provides agent guidance for using a user-approved Permissions Broker API key to make approval-gated Google, GitHub, iCloud CalDAV, and Spotify requests when local credentials are unavailable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stephancill](https://clawhub.ai/user/stephancill)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to route external data access and third-party actions through a user-approved Permissions Broker flow when local credentials are unavailable. It covers request creation, Telegram approval polling, one-time execution, provider-specific URL construction, and secret-handling guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A reusable Permissions Broker API key can expose linked provider data if it is pasted into chat, logs, code, or repository files.

Mitigation: Provide the key through a protected secret such as PB_API_KEY, never commit or log it, and rotate the key if it has been pasted into a conversation.

Risk: Approved broker requests can read or modify linked provider data.

Mitigation: Approve only requests whose upstream URL, method, body, and consent text match the intended task.

Risk: Sending the API key to an unintended broker URL could route credentials or actions through an untrusted service.

Mitigation: Verify the broker URL is exactly the intended Permissions Broker service before creating or polling requests.

Risk: One-time execution means a response may be unavailable after it is consumed.

Mitigation: Parse and persist the needed result immediately after a successful execution.

## Reference(s):

- [Permissions Broker Agent Reference](artifact/references/api_reference.md)
- [iCloud CalDAV Templates](artifact/references/caldav.md)
- [ClawHub Skill Page](https://clawhub.ai/stephancill/skills/permissions-broker)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON, TypeScript, Python, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes approval-gated API request patterns, provider URL examples, polling behavior, and secret-handling guidance.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
