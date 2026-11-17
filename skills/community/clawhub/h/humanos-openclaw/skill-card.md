## Description:

Require verifiable human approval before high-risk agent actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lagosrui](https://clawhub.ai/user/lagosrui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to request, check, and verify human authorization before payments, document signing, sensitive data access, credential rotation, role changes, or other high-risk actions. It can also install an optional OpenClaw guard hook that checks selected tool calls for a valid mandate before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional guard hook should not be treated as a complete security boundary for sensitive actions.

Mitigation: Use separate fail-closed controls for high-risk tools and require a valid mandate before execution.

Risk: The optional guard hook can fail open for sensitive actions and does not enforce mandate constraints before allowing tool execution.

Mitigation: Enforce exact action matching, amount limits, recipient or resource constraints, and validity checks outside the hook before executing the action.

Risk: Custom VIA_API_URL values can point approval checks at an unintended or less trusted service.

Mitigation: Use the default Humanos API for normal use; use custom API URLs only with isolated test credentials.

Risk: VIA API credentials and signing secrets authorize approval-request API calls.

Mitigation: Keep credentials tightly permissioned, store OpenClaw configuration with restrictive file permissions, and rotate secrets if exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lagosrui/skills/humanos-openclaw)
- [Humanos API documentation](https://humanos.mintlify.app/essentials/introduction)
- [W3C Verifiable Credentials Data Model](https://www.w3.org/TR/vc-data-model/)
- [OpenClaw](https://openclaw.ai)
- [Humanos dashboard](https://app.humanos.id)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands, configuration snippets, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VIA_API_KEY and VIA_SIGNATURE_SECRET; uses curl, jq, openssl, and optional Node.js guard hook on macOS/Linux.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
