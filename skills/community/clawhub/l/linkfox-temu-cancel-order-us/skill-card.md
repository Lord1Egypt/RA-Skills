## Description:

Helps agents work with Temu US buyer and seller order-cancellation workflows, including cancellation lists, approvals, appeals, and out-of-stock cancellation status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Temu sellers, operators, and automation agents use this skill to prepare and run US buyer and seller order-cancellation workflows. It supports reviewing buyer cancellation requests, approving cancellations, submitting seller appeal or out-of-stock cancellation requests, and checking request status.

### Deployment Geography for Use:

United States (Temu Partner US workflows)

## Known Risks and Mitigations:

Risk: The skill requires LinkFox and Temu access tokens, which can expose store access if shared or logged.

Mitigation: Use the narrowest Temu token possible, prefer controlled local storage, and avoid passing raw tokens through chat or logs.

Risk: Cancellation and related proxy calls can change order state or affect customer outcomes.

Mitigation: Manually confirm each cancellation, payment, or non-cancellation proxy call and verify target order identifiers before execution.

Risk: Gateway environment overrides could send requests to an unintended host.

Mitigation: Verify gateway environment variables point only to the intended LinkFox HTTPS host before running scripts.

Risk: Full Temu responses can contain retained order or store data in local output files.

Mitigation: Run the skill in a controlled workspace and protect or remove saved response files when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-temu-cancel-order-us)
- [API reference](artifact/references/api.md)
- [Partner US API catalog](artifact/references/partner-us-catalog.md)
- [Cancel Order API index](artifact/references/apis/README.md)
- [Temu access token guide](artifact/references/access-token.md)
- [Authorization flow](artifact/references/authorization-flow.md)
- [Temu Partner US documentation](https://partner-us.temu.com/documentation)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance, shell commands, and JSON API responses printed to stdout or saved as local files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full responses are written under linkfox/<date>/<session>/data; larger responses are summarized on stdout unless inline output is requested.]

## Skill Version(s):

1.0.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
