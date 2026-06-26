## Description: <br>
Browse prediction markets, inspect books and balances, and manage orders or positions in Polymarket - powered by ClawLink. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect Polymarket through ClawLink, browse market data, inspect account state, and preview or manage orders with confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Polymarket order placement or cancellation can affect the user's portfolio. <br>
Mitigation: Preview write actions through ClawLink and require explicit user confirmation before placing or canceling orders. <br>
Risk: Credentials or pairing secrets could be exposed if pasted into chat. <br>
Mitigation: Use ClawLink's pairing and hosted connection flow, keep credentials out of chat, and never echo ClawLink credentials. <br>
Risk: Available Polymarket capabilities can vary by connected account, permissions, scopes, and current ClawLink tool catalog. <br>
Mitigation: Discover and describe live ClawLink tools before use, and report real tool errors instead of guessing capabilities. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/polymarket-markets) <br>
- [ClawLink](https://claw-link.dev) <br>
- [ClawLink Docs](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>
- [ClawLink Source](https://github.com/hith3sh/clawlink) <br>
- [Polymarket Docs](https://docs.polymarket.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and ClawLink tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the live ClawLink tool catalog as the source of truth; trading writes require preview and user confirmation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
