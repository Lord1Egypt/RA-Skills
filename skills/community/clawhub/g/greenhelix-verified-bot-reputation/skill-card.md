## Description: <br>
Guides agents through building cryptographic PnL proof for trading bots using Ed25519 signatures, Merkle claim chains, and GreenHelix API examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading bot operators use this guide to create a cryptographic agent identity, submit signed trading performance metrics, build Merkle proof chains, and expose verifiable reputation data through GreenHelix. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The guide uses sensitive signing keys, bearer tokens, and trading-performance submissions in API examples. <br>
Mitigation: Use a dedicated test signing key first, do not reuse wallet or exchange keys, and keep credentials out of logs, shared files, and committed configuration. <br>
Risk: Examples reference GreenHelix endpoints, and running adapted snippets against production could submit real trading metrics. <br>
Mitigation: Verify whether each snippet targets sandbox or production before running it, and start with sandbox or test data. <br>
Risk: Submitted trading metrics may become discoverable or retained by GreenHelix. <br>
Mitigation: Submit only performance data that is appropriate for external discovery and retention under the user's compliance requirements. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mirni/greenhelix-verified-bot-reputation) <br>
- [GreenHelix Sandbox](https://sandbox.greenhelix.net) <br>
- [GreenHelix API Documentation](https://api.greenhelix.net/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guide with Python and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-supplied AGENT_SIGNING_KEY and may require API bearer tokens when examples are adapted for use.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
