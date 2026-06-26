## Description: <br>
Guides agents in building GreenHelix-based carbon credit trading and CBAM compliance workflows covering credit discovery, MRV verification, escrow-protected trading, portfolio management, and dispute resolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and compliance teams use this guide to design agent-assisted carbon credit discovery, verification, trading, retirement, and CBAM compliance automation with GreenHelix APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Production-style trading, escrow, retirement, dispute, and procurement examples can affect real funds or compliance workflows if connected to live accounts. <br>
Mitigation: Use sandbox or test accounts first, require explicit approval for every financial or compliance action, and add spend limits, monitoring, and emergency stop controls before using real funds. <br>
Risk: The skill requires sensitive GreenHelix credentials for authenticated API access. <br>
Mitigation: Use least-privilege API keys, keep credentials out of committed files, and rotate or revoke keys if exposure is suspected. <br>
Risk: The security evidence flags a mismatch between sandbox-oriented framing and production financial automation guidance. <br>
Mitigation: Review the guide carefully before following examples and validate all workflows against organizational finance, legal, and compliance controls. <br>


## Reference(s): <br>
- [ClawHub Skill Release](https://clawhub.ai/mirni/greenhelix-agent-carbon-credit-trading) <br>
- [GreenHelix Sandbox](https://sandbox.greenhelix.net) <br>
- [GreenHelix API](https://api.greenhelix.net/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown guide with Python code examples and environment variable configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Non-executable guide; authenticated production examples require GREENHELIX_API_KEY, and sandbox testing should come first.] <br>

## Skill Version(s): <br>
1.3.1 (source: evidence.release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
