## Description:

Manage a human's MemoTrader account through the Personal Assistant API by triaging inbox messages, checking credits and balance, managing cliques and conversations, and surfacing high-value opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimbursch1](https://clawhub.ai/user/jimbursch1)

### License/Terms of Use:

MIT-0

## Use Case:

External MemoTrader users use this skill to let an agent monitor their MemoTrader inbox, account balance, notice price, cliques, and conversations. The skill helps identify valuable messages and account updates while leaving replies, credit spending, bids, and notice-price resets to the human.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A live MemoTrader PA key may be exposed if stored in plaintext memory.

Mitigation: Use a dedicated secret store or environment variable for the PA key, avoid writing it to shared memory files, and revoke any key previously stored in plaintext.

Risk: The skill can dismiss messages or change profile and clique settings.

Mitigation: Require explicit user confirmation before dismissing messages or modifying profile and clique settings.

## Reference(s):

- [MemoTrader Platform Overview](references/platform.md)
- [MemoTrader API Reference](references/api.md)
- [MemoTrader](https://memotrader.com)
- [MemoTrader Assistant Key Setup](https://memotrader.com/account/assistant/)
- [ClawHub Skill Page](https://clawhub.ai/jimbursch1/skills/memotrader)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with optional JSON snippets and PowerShell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed API requests, inbox triage results, account-status summaries, and user-confirmation prompts.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
