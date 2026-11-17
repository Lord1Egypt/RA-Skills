## Description:

Send XCH to Twitter users via Go4Me address lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[koba42corp](https://clawhub.ai/user/koba42corp)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to resolve a Twitter handle to a Go4Me Chia address, review the resolved profile details, and send or tip XCH through Sage Wallet after confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can help submit irreversible Chia transactions after user confirmation.

Mitigation: Verify the resolved XCH address, recipient handle, exact mojo amount, and fee before approving any send or tip action.

Risk: Natural-language payment requests can be ambiguous or misread.

Mitigation: Use explicit command syntax for payment actions and avoid sending funds from vague requests until stricter handle validation, address validation, and amount limits are added.

## Reference(s):

- [Go4Me skill page](https://clawhub.ai/koba42corp/skills/go4me)
- [Go4Me](https://go4.me/)
- [Chia Network](https://www.chia.net/)
- [Sage Wallet](https://github.com/xch-dev/sage)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown and command output with JSON lookup results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Sage Wallet for XCH transaction submission.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
