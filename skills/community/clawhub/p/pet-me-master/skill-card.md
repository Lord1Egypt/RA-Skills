## Description:

Batch-pet Aavegotchis on Base via Bankr with cooldown checks, reminder automation, and natural-language routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaigotchi](https://clawhub.ai/user/aaigotchi)

### License/Terms of Use:

MIT-0

## Use Case:

External Aavegotchi users use this skill to check on-chain petting cooldowns, batch-pet owned or delegated gotchis on Base through Bankr, and configure reminders or fallback automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make unattended wallet-linked blockchain actions through Bankr.

Mitigation: Use dry-run and status checks first, avoid enabling cron, fallback auto-pet, or recurring loops unless unattended actions are intended, and monitor submitted transactions.

Risk: Bankr credentials and configurable API endpoints affect transaction submission.

Mitigation: Use a dedicated, narrowly scoped Bankr key, protect local config files, avoid environments where untrusted code can change BANKR_API_URL, and rotate credentials after untrusted execution.

Risk: Natural-language pet commands can route to mutating batch pet scripts.

Mitigation: Use transaction dry-run mode or manual confirmation for ambiguous requests before allowing the skill to submit a Bankr transaction.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaigotchi/skills/pet-me-master)
- [aaigotchi publisher profile](https://clawhub.ai/user/aaigotchi)
- [Aavegotchi contract information](artifact/references/contract-info.md)
- [Base mainnet RPC](https://mainnet.base.org)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger Bankr API calls and blockchain transactions when the user runs mutating scripts; dry-run and status modes are available.]

## Skill Version(s):

2.4.4 (source: server release, artifact/clawhub.json, CHANGELOG top entry)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
