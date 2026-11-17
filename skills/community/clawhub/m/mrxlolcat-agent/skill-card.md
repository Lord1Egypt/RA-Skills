## Description:

Master AI Automation Agent for the Farcaster ecosystem. Specializes in autonomous on-chain actions, cross-chain bridging via LI.FI, and long-term FID memory management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrxlolcat](https://clawhub.ai/user/mrxlolcat)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to coordinate Farcaster interactions, wallet monitoring, cross-chain bridge guidance, and long-term FID-linked memory for the MRX LOLCAT agent experience.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide users into bridge or swap flows where chain, token, amount, destination, route, and fee details can materially affect funds.

Mitigation: Require the user to verify every chain, token, amount, fee recipient, route, destination, and transaction link in their own wallet interface before signing.

Risk: The skill may draft or publish Farcaster content and external TTS output that could expose unintended information or misrepresent user intent.

Mitigation: Present cast text, generated voice content, and links for explicit user review before publishing or attaching them.

Risk: The skill stores transaction-related context in long-term memory without enough documented scoping or privacy controls.

Mitigation: Store only necessary public transaction context, avoid private keys or seed phrases, and allow users to decline or limit memory use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mrxlolcat/skills/mrxlolcat-agent)
- [MRX LOLCAT Agent homepage](https://mrxlolcat-agent.vercel.app)
- [Agent metadata endpoint](https://mrxlolcat-agent.vercel.app/agent.json)
- [MCP endpoint](https://mrxlolcat-agent.vercel.app/api/mcp)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown]

**Output Format:** [Plain text or Markdown responses with wallet, bridge, monitoring, and Farcaster action guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include route summaries, wallet-status summaries, cast drafts, transaction-link guidance, and reminders that users must verify and sign actions in their own wallet interface.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
