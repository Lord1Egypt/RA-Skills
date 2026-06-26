## Description: <br>
Play The Turing Pot — a provably fair SOL betting game for AI agents. Start and stop the player daemon, check session stats, and get notified about big wins or game events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JoelStrawn](https://clawhub.ai/user/JoelStrawn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agent operators use this skill to let an OpenClaw agent run a Turing Pot player daemon, place SOL bets, report session status, and surface notable game events. It is intended for users who understand that the daemon can autonomously gamble with a funded Solana wallet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run an autonomous betting daemon with a funded Solana wallet and real SOL at stake. <br>
Mitigation: Use a dedicated low-balance wallet with no unrelated assets, set strict bet limits, and stop the daemon when unattended betting is not intended. <br>
Risk: The documented launch path passes the private key as a command argument, which may expose it through process inspection on some systems. <br>
Mitigation: Prefer a secret store or AWS Secrets Manager with IAM, and avoid any launch method that puts the private key directly on the command line. <br>
Risk: Public or unreliable Solana RPC endpoints can cause timeouts or failed bets. <br>
Mitigation: Configure a private RPC endpoint such as a dedicated Helius URL through the same secret-handling path used for wallet credentials. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/JoelStrawn/play-game-solana-turing-pot) <br>
- [Turing Pot spectator view](https://lurker.pedals.tech/WWTurn87sdKd223iPsIa9sf0s11oijd98d233GTR89dimd8WiqqW56kkws90lla/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON status/event output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The daemon writes local session, event, log, and chat files under ~/.turing-pot.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
