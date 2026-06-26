## Description: <br>
全渠道选品 Agent — 拉齐社媒端、SEO端、投放端数据，帮助运营同学确定待上线需求。触发词：选品、社媒热点、SEO调研、竞品广告、Facebook Ads、TikTok趋势。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lygjoey](https://clawhub.ai/user/lygjoey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations, growth, and product teams use this skill to collect social, SEO, advertising, and KOL trend signals for AI visual-product research and launch planning. It supports full or single-channel research pipelines and produces Slack-ready reports plus source JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports under-scoped credential handling and artifact code reads tokens from shell profile files. <br>
Mitigation: Use dedicated least-privilege API tokens, provide them through a controlled runtime environment, and remove shell-profile credential loading before deployment. <br>
Risk: The security evidence reports runtime environment mutation, and artifact code can install dependencies at runtime. <br>
Mitigation: Review and pin dependencies ahead of use, install them in an isolated environment, and disable runtime package installation. <br>
Risk: The security evidence reports off-purpose adult or sensitive trend data in stored outputs. <br>
Mitigation: Apply strict source allowlists plus NSFW and off-topic filters before using outputs for product or marketing decisions. <br>
Risk: The trend methodology says automated scores are only an initial screen and that cultural context requires human review. <br>
Mitigation: Require human review of trend fit, visual quality, and cultural context before turning recommendations into launch decisions. <br>


## Reference(s): <br>
- [Omni Channel Agent on ClawHub](https://clawhub.ai/lygjoey/omni-channel-agent) <br>
- [Publisher profile: lygjoey](https://clawhub.ai/user/lygjoey) <br>
- [Trend Methodology](artifact/TREND_METHODOLOGY.md) <br>
- [Apify API endpoint](https://api.apify.com/v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Slack-style text reports, JSON data files, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes timestamped reports and channel-specific JSON files under output/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
