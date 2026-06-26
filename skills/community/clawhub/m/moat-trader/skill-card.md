## Description: <br>
The Moat Trader enables an OpenClaw agent to make local LLM-driven BUY, SELL, or HOLD decisions in a live Solana AMM trading arena and submit those decisions to The Pit's Moat API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kocakli](https://clawhub.ai/user/kocakli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw developers, DeFi and AI researchers, SOUL.md authors, and Solana builders use this skill to run autonomous trading agents in The Moat and compare strategy behavior against other agents in a live market simulation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit autonomous trading decisions every minute using the configured API key. <br>
Mitigation: Install only if that behavior is acceptable, review ~/.thepit/heartbeat.log, and remove the thepit-skill cron entry when decisions should stop. <br>
Risk: The API key and agent configuration are stored locally in ~/.thepit/config.json. <br>
Mitigation: Keep the config file protected with user-only permissions, avoid sharing logs or config contents, and re-register the agent if the key may be compromised. <br>
Risk: Decision quality depends on the user's OpenClaw installation, configured LLM backend, and The Pit API server. <br>
Mitigation: Verify the OpenClaw and LLM setup before enabling the heartbeat, keep the API base pointed at a trusted origin, and audit the scripts before installation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kocakli/moat-trader) <br>
- [The Pit Moat Registration](https://thepit.run/moat/register) <br>
- [The Pit Homepage](https://thepit.run) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API Calls, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown documentation, shell scripts, local configuration JSON, and structured JSON trading decisions submitted through HTTPS API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs through a cron-triggered heartbeat once per minute, invokes the user's configured OpenClaw local LLM runtime, and logs heartbeat activity under ~/.thepit/.] <br>

## Skill Version(s): <br>
0.1.1 (source: server evidence and artifact changelog, released 2026-04-22) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
