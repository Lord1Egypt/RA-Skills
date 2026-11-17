## Description:

Assesses an IP address by querying IP intelligence sources, assigning a 0-100 risk score, and producing a report with Claude Code usage guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kuiilabs](https://clawhub.ai/user/kuiilabs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Claude Code users use this skill to inspect IP reputation signals, identify proxy/VPN/Tor or data-center indicators, and decide whether an IP should be used cautiously. The skill can also create Markdown-style reports for record keeping when an IP receives a high score.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queried IP addresses are sent to third-party IP and reputation services.

Mitigation: Use the skill only for IPs you are comfortable disclosing to those services, and review the called endpoints before execution.

Risk: The Python scanner writes high-scoring reports automatically to a hardcoded Obsidian path.

Mitigation: Run with --no-save when persistence is not desired, or edit the save path before use in another environment.

Risk: Claude compatibility and ban-risk scores are unofficial heuristics.

Mitigation: Treat the score as advisory and verify account, network, and policy risk through authoritative platform guidance.

## Reference(s):

- [IP risk guide](references/ip-risk-guide.md)
- [ClawHub skill page](https://clawhub.ai/kuiilabs/skills/ip-risk-scanner)
- [Scamalytics](https://scamalytics.com)
- [BrowserLeaks](https://browserleaks.com)
- [ip-api.com JSON endpoint](http://ip-api.com/json/{IP})
- [Claude account ban analysis](https://www.augmunt.com/blog/claude-account-ban-solutions-deep-dive-2026/)
- [Claude Code source leak and ban policy analysis](https://blog.laozhang.ai/en/posts/claude-code-source-leak-ban-policy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Console text and Markdown reports with score tables, external-check links, and usage recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports scoring 80 or higher are written automatically to a fixed Obsidian vault path by default; the Python script supports --no-save.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
