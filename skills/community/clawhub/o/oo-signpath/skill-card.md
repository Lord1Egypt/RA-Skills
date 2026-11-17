## Description:

Use this skill to read, create, and update SignPath data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to inspect SignPath signing policies and request status, and to submit hash-signing requests through SignPath. It assumes the oo CLI is installed, signed in, and connected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unverified downloaded CLI code; the installer and hosted service were not verified.

Mitigation: Review and install the CLI separately. Disable automatic skill synchronization with OO_SKILLS_SYNC_DISABLED=1 when appropriate.

Risk: Hash-signing requests use the connected account and can submit signing payloads.

Mitigation: Use appropriately scoped credentials and review the exact payload before running fast_sign_hash.

Risk: The security review says setup can make broader agent changes that are not fully explained.

Mitigation: Review CLI setup behavior and the resulting agent changes before enabling setup.

## Reference(s):

- [oo CLI Command Reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [SignPath REST API Documentation](https://docs.signpath.io/crypto-providers/rest-api)
- [SignPath](https://signpath.io/)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, JSON, Text]

**Output Format:** [Shell commands with JSON request payloads and structured JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include signing policy details, signing request status, or a signature result.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
