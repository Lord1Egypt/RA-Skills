## Description: <br>
IP Risk Scanner evaluates supplied IP addresses with heuristic risk scoring, lookup results, and Claude Code usage guidance, and can save high-scoring Markdown reports locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kuiilabs](https://clawhub.ai/user/kuiilabs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Claude Code users can use this skill to inspect an IP address, review geolocation and proxy/VPN/Tor signals, and receive a Markdown-style safety report with usage guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The score and Claude compatibility wording may be mistaken for official compliance or account-safety proof. <br>
Mitigation: Present results as heuristic guidance only and independently verify account, network, and service-policy requirements before relying on them. <br>
Risk: IP addresses are sent to third-party lookup services during checks. <br>
Mitigation: Avoid scanning sensitive IPs unless the user accepts disclosure to external services. <br>
Risk: High-scoring IP reports may be written to a local Obsidian vault. <br>
Mitigation: Use the no-save option or review local report paths and retention practices before running the scanner. <br>


## Reference(s): <br>
- [IP risk guide](references/ip-risk-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/kuiilabs/ip-risk-scanner) <br>
- [Publisher profile](https://clawhub.ai/user/kuiilabs) <br>
- [Scamalytics](https://scamalytics.com) <br>
- [BrowserLeaks](https://browserleaks.com) <br>
- [Claude account ban analysis](https://www.augmunt.com/blog/claude-account-ban-solutions-deep-dive-2026/) <br>
- [Claude Code source leak ban policy analysis](https://blog.laozhang.ai/en/posts/claude-code-source-leak-ban-policy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Console text and Markdown reports with YAML frontmatter and tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local Markdown reports for IPs scoring 80 or higher unless saving is disabled.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
