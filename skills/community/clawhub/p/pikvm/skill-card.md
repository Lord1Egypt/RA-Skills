## Description:

Control and inspect PiKVM devices over the PiKVM HTTP API for power, HID input, screen capture, OCR, virtual media, and switch-port operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[didyouexpectthat](https://clawhub.ai/user/didyouexpectthat)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect and administer PiKVM-managed machines through authenticated HTTP API calls, including read-only status checks and explicitly approved remote-control actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send powerful PiKVM credentials and commands to network destinations.

Mitigation: Use a dedicated least-privilege PiKVM account, keep HTTPS certificate verification enabled, and avoid untrusted or plaintext PIKVM_URL values.

Risk: Power, HID, switch, and virtual-media operations can affect remote machines in high-impact ways.

Mitigation: Require explicit confirmation before state-changing operations and re-read the relevant PiKVM state after each change.

Risk: Remote media download operations make the PiKVM fetch a URL from its own network.

Mitigation: Treat remote media URLs as sensitive and use only trusted media sources that are appropriate for the PiKVM network.

## Reference(s):

- [PiKVM API documentation](https://docs.pikvm.org/api/)
- [PiKVM API reference notes](references/api-reference.md)
- [ClawHub skill page](https://clawhub.ai/didyouexpectthat/skills/pikvm)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save snapshot image files when explicitly requested; command results should not expose passwords, TOTP values, or session cookies.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
