## Description:

MessageGuard filters outgoing text for sensitive data using regex patterns and configurable actions such as masking, blocking, or warning before a message is sent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andrewandrewsen](https://clawhub.ai/user/andrewandrewsen)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill as a pre-send guard for outgoing messages that may contain secrets, credentials, or sensitive data. It helps mask lower-risk matches, block high-risk matches, and surface warnings before content is transmitted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Blocked outputs and detection details may expose the sensitive content the skill detected.

Mitigation: Do not transmit blocked result messages; redact or omit blocked output and detection snippets before sharing them.

Risk: Detection logs may contain sensitive snippets or blocked-event metadata.

Mitigation: Keep detection logging disabled unless needed, restrict log file permissions, minimize retained fields, and apply an explicit retention policy.

Risk: Configuration failures fall back to defaults, which may be inappropriate for high-sensitivity workflows.

Mitigation: Review or patch the script to fail closed for required configurations before using it with highly sensitive messages.

## Reference(s):

- [MessageGuard Skill Page](https://clawhub.ai/andrewandrewsen/skills/messageguard)
- [Config Schema Reference](artifact/references/config-schema.md)
- [Integration Guide](artifact/references/integration.md)
- [Built-in Pattern Library](artifact/references/patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON results and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The filter script returns JSON containing blocked status, filtered or original message text, detections, and warnings.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
