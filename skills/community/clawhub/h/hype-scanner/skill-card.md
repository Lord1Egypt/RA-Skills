## Description: <br>
Real-time crypto and stock hype detection using Reddit, CoinGecko, DEXScreener, and StockTwits with AI-powered signal validation using a local Ollama model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[peti0402](https://clawhub.ai/user/peti0402) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and trading-oriented users use this skill to configure an unattended local scanner that writes market-hype alerts for crypto tokens and stocks and routes pending alerts into OpenClaw or Telegram workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review notes under-documented trading-account updates may include account details such as equity and positions in the Telegram alert flow. <br>
Mitigation: Review the skill before installing, avoid connecting brokerage credentials, and do not add or enable trading-monitor behavior unless it has been reviewed and is explicitly intended. <br>
Risk: The skill is designed for unattended scheduled scans and Telegram delivery, which can send market alerts continuously without manual review. <br>
Mitigation: Run it only in an environment where scheduled scans and outbound alerts are expected, and periodically review generated alerts and logs. <br>


## Reference(s): <br>
- [Hype Scanner on ClawHub](https://clawhub.ai/peti0402/hype-scanner) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with JavaScript, shell, VBS, and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local scanner setup guidance and alert-file workflow configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
