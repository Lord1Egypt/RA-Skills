## Description: <br>
Tracks and reports multi-group stock portfolios with daily snapshots, Yahoo Finance prices, P&L analytics, holding updates, and optional Feishu or Telegram notifications for A-share, Hong Kong, and U.S. markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Stepuuu](https://clawhub.ai/user/Stepuuu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query and update portfolio holdings, cash, and fund balances, generate daily snapshots and reports, and optionally send reports through Feishu or Telegram. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify portfolio holdings, cash balances, fund values, and rebalance records. <br>
Mitigation: Require explicit user confirmation before holdings, cash, fund, rebalance, remove, pipeline, or report-send actions, and review changed portfolio files after updates. <br>
Risk: Portfolio reports may contain private financial information and can be sent to external Feishu or Telegram channels. <br>
Mitigation: Keep notification credentials unset unless needed, verify the destination before enabling report sends, and avoid sharing reports with unintended recipients. <br>
Risk: Setup clones and installs remote engine code that is not pinned by the artifact. <br>
Mitigation: Review or otherwise trust the cloned repository and dependencies before installation; use a pinned revision in controlled deployments. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands, JSON/tool-call results, and generated portfolio reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can update local portfolio JSON/CSV records and optionally send portfolio reports through configured notification credentials.] <br>

## Skill Version(s): <br>
1.2.0 (source: evidence.release.version, SKILL.md frontmatter, changelog dated 2026-03-10) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
