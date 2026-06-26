## Description: <br>
Coinbase helps an agent use the OOMOL Coinbase connector to search and read Coinbase account data without handling raw Coinbase tokens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill when they want an agent to retrieve Coinbase account information through an OOMOL-connected Coinbase account. The documented actions list accessible Coinbase Advanced Trade brokerage accounts and fetch a specific account by UUID. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to sensitive Coinbase account information through OOMOL-managed credentials. <br>
Mitigation: Install only when you trust OOMOL to mediate Coinbase access and intend the agent to read Coinbase account data. <br>
Risk: Future or connector-discovered write, trading, or transfer actions could affect Coinbase state if treated like the documented read actions. <br>
Mitigation: Treat those actions as out of scope unless the agent shows the exact payload and receives explicit user approval. <br>


## Reference(s): <br>
- [Coinbase homepage](https://www.coinbase.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-coinbase) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before building action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
