## Description: <br>
Tracks cross-platform trending topics, analyzes lifecycle and resonance signals, and generates structured daily hotspot reports with product-manager-oriented content suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gold3bear](https://clawhub.ai/user/gold3bear) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product managers, and content operators use this skill to collect multi-platform hot topics, monitor competitor or industry keywords, compare topic spread, and produce daily Markdown reports or Feishu updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is a broad web-scraping and reporting tool that can contact many public platforms and store local archives. <br>
Mitigation: Review enabled platforms before use, run it in a controlled workspace, and retain only data that the operator is allowed to collect and store. <br>
Risk: The security evidence says the platform enablement logic may contact disabled platforms. <br>
Mitigation: Fix and verify platform filtering before scheduled or production runs, especially when API keys, cookies, or proxies are configured. <br>
Risk: Feishu notification and bitable flows use local tokens and hardcoded recipient or app identifiers. <br>
Mitigation: Replace bundled Feishu identifiers with the operator's own configuration and keep tokens in a protected local secret store. <br>
Risk: Instagram collection may use plaintext session cookies and authenticated traffic may be sent through a local proxy. <br>
Mitigation: Avoid plaintext session cookies, use only trusted proxies, and disable authenticated collectors unless their credential handling has been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gold3bear/hot-radar) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON data archives, console output, and optional Feishu message or bitable updates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Daily mode writes dated report and data files; optional flags can sync to Feishu bitable or send Feishu notifications.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
