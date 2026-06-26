## Description: <br>
DEPRECATED. Use jun-invest-option-master-agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gm4leejun-stack](https://clawhub.ai/user/gm4leejun-stack) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this deprecated installer alias when migrating to or installing the jun-invest-option-master-agent investment-research workspace. The bundled agent assets support approval-packet generation for cash-secured put and covered-call workflows, with human approval required before any trade. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package is labeled as a deprecated installer alias but includes an active investment-research agent and automatic workspace update instructions. <br>
Mitigation: Install only when intending to run the local investment-research agent; review the upgrade flow, workspace target, agent registration, and gateway restart notes before use. <br>
Risk: Investment and options research outputs may be incorrect, stale, or unsuitable for a user's portfolio. <br>
Mitigation: Keep human approval mandatory for every trade, enforce the documented no-leverage and CSP/covered-call boundaries, and review validation reports before acting. <br>
Risk: Market-data dependencies such as Futu OpenD, yfinance, and Stooq may be unavailable, incomplete, or permission-limited. <br>
Mitigation: Check source timestamps, data quality, OpenD availability, and fallback behavior; treat missing or low-confidence data as a reason to defer approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gm4leejun-stack/jun-invest-option-master-installer) <br>
- [OpenClaw documentation](https://docs.openclaw.ai/) <br>
- [Futu OpenAPI documentation](https://openapi.futunn.com/futu-api-doc/intro/intro.html) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown approval packets, JSON validation reports, YAML/JSON configuration, Python utilities, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advisory investment-research outputs require human trade approval; installer behavior may copy local workspace assets and register an OpenClaw agent.] <br>

## Skill Version(s): <br>
0.99.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
