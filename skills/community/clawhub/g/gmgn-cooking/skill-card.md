## Description: <br>
[FINANCIAL EXECUTION] Create and launch meme coins and crypto tokens on launchpads (Pump.fun, FourMeme, Bonk, BAGS, Flap, Klik, Clanker, etc.) via bonding curve fair launch, or query token creation stats by launchpad via GMGN API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gmgnai](https://clawhub.ai/user/gmgnai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide an agent through GMGN CLI token-launch workflows, token creation statistics, credential setup, confirmation prompts, and post-launch order polling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Token launches are real, irreversible blockchain transactions that spend funds. <br>
Mitigation: Require explicit user confirmation before every create command and confirm the chain, platform, wallet, token details, and buy amount in human-readable units. <br>
Risk: The skill handles high-impact API and private key material for signed token creation. <br>
Mitigation: Keep credentials out of chat where possible, prefer manual credential configuration, restrict local key files, and delete temporary key material after setup. <br>
Risk: Persistent launch preferences or advanced fee settings can affect later transactions. <br>
Mitigation: Save advanced launch preferences only when the user intends reuse, and reconfirm fee splits, auto-sell settings, and platform-specific options before execution. <br>
Risk: Automated retrying can duplicate or worsen financial operations after rate limits or pending orders. <br>
Mitigation: Do not auto-resubmit create commands; wait for the reset time or order status and ask for fresh confirmation before retrying. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gmgnai/gmgn-cooking) <br>
- [gmgn-swap related skill](https://github.com/GMGNAI/gmgn-skills/tree/main/skills/gmgn-swap) <br>
- [gmgn-token related skill](https://github.com/GMGNAI/gmgn-skills/tree/main/skills/gmgn-token) <br>
- [gmgn-market related skill](https://github.com/GMGNAI/gmgn-skills/tree/main/skills/gmgn-market) <br>
- [gmgn-track related skill](https://github.com/GMGNAI/gmgn-skills/tree/main/skills/gmgn-track) <br>
- [gmgn-portfolio related skill](https://github.com/GMGNAI/gmgn-skills/tree/main/skills/gmgn-portfolio) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit confirmation before token creation commands; may include command outputs or transaction receipt summaries.] <br>

## Skill Version(s): <br>
1.4.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
