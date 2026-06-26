## Description: <br>
Use a Bash CLI to query Kraken Spot and Futures APIs, inspect account state, run guarded trading and funding actions, and work with Kraken websocket payloads using OpenClaw-managed secrets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oscraters](https://clawhub.ai/user/oscraters) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to let an agent work with Kraken Spot, Futures, funding, earn, order, account, and websocket workflows through a local Bash CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access high-impact Kraken account, trading, funding, and futures workflows when credentials are present. <br>
Mitigation: Use least-privilege Kraken API keys, avoid withdrawal permissions unless necessary, and require operator confirmation before state-changing commands. <br>
Risk: Shell configuration can execute before the skill's safeguards run if OPENCLAW_KRAKEN_CONFIG points to an untrusted file. <br>
Mitigation: Keep OPENCLAW_KRAKEN_CONFIG pointed only at a trusted file owned by the operator, and avoid storing plaintext secrets in that file. <br>
Risk: Endpoint or confirmation settings can change the safety posture of trading and funding commands. <br>
Mitigation: Review settings that disable confirmation or change API endpoints before using trading, funding, earn, futures, or transfer commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oscraters/kraken-cli) <br>
- [Source homepage](https://github.com/oscraters/kraken-skill.git) <br>
- [OpenClaw secrets documentation](https://docs.openclaw.ai/gateway/secrets) <br>
- [Configuration guide](docs/configuration.md) <br>
- [Security notes](docs/security.md) <br>
- [Usage examples](docs/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit JSON API responses from Kraken commands when the CLI is executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
