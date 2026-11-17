## Description:

Use this skill to guide an agent through policy-controlled OmniClaw CLI payments, x402 paid URL access, balance and ledger inspection, and explicitly approved paid endpoint serving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abiorh001](https://clawhub.ai/user/abiorh001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect OmniClaw balances and ledger entries, check payment policy, pay x402 URLs or USDC recipients, and expose paid endpoints only when the owner explicitly requests it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide high-impact financial actions through OmniClaw payment commands.

Mitigation: Use a trusted OmniClaw CLI and Financial Policy Engine, provide a narrowly scoped agent token, check policy with can-pay before new recipients, and stop on policy or balance failures.

Risk: OMNICLAW_OWNER_TOKEN can grant owner approval authority if provided to the agent runtime.

Mitigation: Do not set OMNICLAW_OWNER_TOKEN unless a human intentionally wants this agent to approve confirmations for the current run.

Risk: omniclaw-cli serve exposes a network-accessible endpoint and --exec runs a host command.

Mitigation: Use serve only after explicit owner request with an approved command, price, endpoint, and port, preferably inside an isolated runtime.

Risk: The reference generator is flagged by security guidance as unsafe when run with elevated privileges.

Mitigation: Do not run the reference generator as a privileged user until its output path and environment handling are fixed.

## Reference(s):

- [OmniClaw CLI Reference](references/cli-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/abiorh001/skills/omniclaw)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and CLI flag references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires omniclaw-cli, OMNICLAW_SERVER_URL, and OMNICLAW_TOKEN; OMNICLAW_OWNER_TOKEN is optional for intentional owner approvals.]

## Skill Version(s):

0.0.8 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
