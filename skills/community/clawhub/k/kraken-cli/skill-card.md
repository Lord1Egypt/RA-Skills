## Description:

Use a Bash CLI to query Kraken Spot and Futures APIs, inspect account state, run guarded trading and funding actions, and work with Kraken websocket payloads using OpenClaw-managed secrets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oscraters](https://clawhub.ai/user/oscraters)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to let an agent prepare and run Kraken market-data, account, funding, trading, futures, and websocket CLI workflows with guarded secret handling and confirmation for state-changing actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access financial account functions, including trading, funding, and withdrawal-related Kraken workflows.

Mitigation: Use least-privileged Kraken API keys, avoid withdrawal or trading permissions unless required, and require explicit confirmation before state-changing actions.

Risk: Untrusted OPENCLAW_KRAKEN_CONFIG files can alter the runtime environment used by the CLI.

Mitigation: Use only reviewed configuration files and keep secrets supplied through controlled environment or OpenClaw secret references.

Risk: API and websocket host overrides could route requests outside the intended Kraken endpoints.

Mitigation: Keep REST and websocket hosts pinned to Kraken-controlled endpoints and review any host override before use.

Risk: Websocket message files may transmit local file contents through agent-driven websocket requests.

Mitigation: Use only reviewed message files and exclude local secrets, credentials, or unrelated sensitive data from websocket payloads.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/oscraters/skills/kraken-cli)
- [Skill Homepage](https://github.com/oscraters/kraken-skill.git)
- [OpenClaw Secrets](https://docs.openclaw.ai/gateway/secrets)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce commands that call Kraken APIs and may return API response text or formatted JSON when jq modes are used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
