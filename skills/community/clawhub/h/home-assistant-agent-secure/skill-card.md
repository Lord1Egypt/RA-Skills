## Description:

Control Home Assistant smart home devices securely using the Assist (Conversation) API while routing natural-language commands through Home Assistant's built-in NLU with a restricted non-admin user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[szafranski](https://clawhub.ai/user/szafranski)

### License/Terms of Use:

MIT

## Use Case:

Developers and smart-home operators use this skill to let an agent send natural-language commands to Home Assistant Assist while limiting access to a restricted non-admin Home Assistant user and the Conversation API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A long-lived Home Assistant token can retain access until revoked.

Mitigation: Use a dedicated non-admin Home Assistant user with the smallest practical device and entity access, and revoke or rotate the token if it may have been exposed.

Risk: The default curl example allows insecure TLS for self-signed Home Assistant certificates.

Mitigation: Remove curl -k when Home Assistant is configured with trusted certificates, and only keep it when the certificate trust decision has been made explicitly.

Risk: Storing the Home Assistant token in shell profiles or broadly readable files can expose smart-home access.

Mitigation: Prefer a locked-down token file or managed environment injection, avoid echoing the token, and restrict file permissions.

Risk: Trusted Networks login bypass can undermine the restricted-user security model.

Mitigation: Set allow_bypass_login to false for the trusted_networks auth provider or remove that provider before using the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/szafranski/skills/home-assistant-agent-secure)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, API Calls, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, HOME_ASSISTANT_URL, and HOME_ASSISTANT_TOKEN; relays Home Assistant Assist responses to the user.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
