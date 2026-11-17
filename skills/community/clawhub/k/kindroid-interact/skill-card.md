## Description:

Interact with Kindroid companions via their official API. Send messages, handle chat breaks, and manage multi-bot conversations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lumenlemons](https://clawhub.ai/user/lumenlemons)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an agent send authenticated messages to Kindroid companions, initiate chat breaks, check companion status, and route conversations across configured companions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a persistent Kindroid API key and uses it to send authenticated messages and chat-break requests.

Mitigation: Use a dedicated, revocable API key; keep the credentials file private; and rotate or revoke the key when access is no longer needed.

Risk: The shell wrapper uses a shared /tmp rate-limit file, which can be unsafe on shared multi-user systems.

Mitigation: Avoid the shell wrapper on shared systems until the temporary-file handling is fixed, or run it only in a trusted single-user environment.

Risk: The security guidance flags JSON escaping issues in the shell wrapper.

Mitigation: Prefer reviewed inputs and the Node.js wrapper for structured API calls until shell argument escaping is corrected.

Risk: The advertised webhook feature is not supported by the provided implementation.

Mitigation: Do not rely on webhook behavior without separate implementation and review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lumenlemons/skills/kindroid-interact)
- [Kindroid](https://kindroid.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration JSON examples, and API response text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq for the shell wrapper; stores a persistent Kindroid API key in a local credentials file.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
