## Description: <br>
Generates a KokoChat connection code through OpenClaw's official `openclaw qr` device-pair flow and relay tunnel, then guides the user to verify and approve or revoke the paired phone. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[komako-workshop](https://clawhub.ai/user/komako-workshop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw Gateway users and developers use this skill to pair a KokoChat mobile client by generating a relay-backed setup code and checking device approval and scopes after redemption. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pairing creates KokoChat relay state and may require running KokoChat relay connector processes for Gateway access. <br>
Mitigation: Install only when relay-based Gateway access is acceptable, review the resulting relay/device state, and manage or remove connector state after pairing as needed. <br>
Risk: The paired phone may receive device scopes that differ from KokoChat's expected read/write access depending on OpenClaw version or Gateway policy. <br>
Mitigation: Inspect `openclaw devices list` after redemption and revoke or remove the device if its identity or scopes do not match the owner's consent. <br>
Risk: Connection setup material includes a gateway-signed bootstrap token and should not expose raw Gateway authentication tokens. <br>
Mitigation: Return only the generated setup code, avoid printing raw `gateway.auth.token`, and use the official `openclaw qr` flow rather than self-signing tokens. <br>


## Reference(s): <br>
- [Kokochat Pairing on ClawHub](https://clawhub.ai/komako-workshop/kokochat-pairing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown containing a fenced raw KokoChat connection code plus concise follow-up commands or guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The connection code should be returned without exposing raw Gateway authentication tokens.] <br>

## Skill Version(s): <br>
0.4.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
