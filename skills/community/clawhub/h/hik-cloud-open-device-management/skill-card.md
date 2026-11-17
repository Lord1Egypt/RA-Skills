## Description:

Manages Hik-Cloud Open Platform device operations including registration, deletion, renaming, detail and list queries, counts, status checks, and reboots while handling access-token refresh.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hik-cloud-open](https://clawhub.ai/user/hik-cloud-open)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams with Hik-Cloud Open Platform credentials use this skill to manage device lifecycle, inventory, status, and reboot workflows through agent-issued commands. It is intended for controlled device administration where credentials and high-impact operations are reviewed before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses powerful Hik-Cloud credentials that can manage cloud-connected devices.

Mitigation: Use tightly scoped credentials, avoid sharing tokens in prompts or logs, and rotate credentials if exposure is suspected.

Risk: Delete and reboot commands can disrupt devices or remove device registrations.

Mitigation: Confirm the target device serial number and business impact before invoking delete or reboot operations.

Risk: Custom base URLs can redirect credentialed requests to an untrusted endpoint.

Mitigation: Use the default Hik-Cloud endpoint unless the custom endpoint is controlled and trusted.

Risk: The token cache stores access-token material on disk.

Mitigation: Protect the token cache path with appropriate filesystem permissions and clear the cache when no longer needed.

## Reference(s):

- [Authentication notes](artifact/references/auth.md)
- [Device management reference summary](artifact/references/device-management.md)
- [Hik-Cloud Open Platform device management documentation](https://pic.hik-cloud.com/opencustom/apidoc/online/open/d1856283d9d944719474b24b6374e351.html)
- [ClawHub skill page](https://clawhub.ai/hik-cloud-open/skills/hik-cloud-open-device-management)
- [Publisher profile](https://clawhub.ai/user/hik-cloud-open)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command results may include summarized text or structured JSON containing request context and raw API response data.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
