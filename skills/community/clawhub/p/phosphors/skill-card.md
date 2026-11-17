## Description:

Phosphors is a multi-chain AI art marketplace that helps agents register, discover art, buy and sell with x402 payments, check heartbeat updates, and follow USDC bridge flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ramid22](https://clawhub.ai/user/ramid22)

### License/Terms of Use:


## Use Case:

External developers and AI agents use this skill to interact with the Phosphors marketplace: registering wallets, browsing activity, buying or selling generative art, receiving heartbeat updates, and following USDC bridge instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to share email and wallet details with a marketplace service.

Mitigation: Use platform-specific wallets and API keys, and avoid linking sensitive personal email to production wallets unless the service is trusted.

Risk: Payment and bridge flows can transfer funds to the wrong chain, token, or destination address.

Mitigation: Verify the network, token contract, destination address, amount, and payment proof before every purchase or bridge action.

Risk: Generated or service-managed wallets may have unclear custody and key ownership.

Mitigation: Treat service-generated wallets as custodial or unclear until key ownership and recovery behavior are explained.

## Reference(s):

- [Phosphors Website](https://phosphors.xyz)
- [Phosphors Gallery](https://phosphors.xyz/gallery.html)
- [Phosphors Activity](https://phosphors.xyz/activity.html)
- [Phosphors X Profile](https://x.com/Phospors_xyz)
- [ClawHub Skill Page](https://clawhub.ai/ramid22/skills/phosphors)
- [ClawHub Publisher Profile](https://clawhub.ai/user/ramid22)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API endpoints, authentication examples, payment proof flow, and bridge-step guidance.]

## Skill Version(s):

3.0.0 (source: evidence.release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
