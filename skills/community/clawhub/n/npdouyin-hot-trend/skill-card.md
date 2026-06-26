## Description: <br>
Retrieves Douyin hot-trend and hot-search ranking data, including titles, popularity values, detail links, tags, content types, and optional cover image URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yezi1985201](https://clawhub.ai/user/yezi1985201) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and social media operators use this skill to retrieve Douyin trending topics for hotspot monitoring, trend analysis, marketing planning, and social media operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Under-disclosed Telegram handoff behavior in the cron workflow could send generated trend messages to an unexpected destination. <br>
Mitigation: Do not enable Telegram or cron workflows unless the destination is removed or explicitly configured by the installing user. <br>
Risk: The helper command path needs input review before installation. <br>
Mitigation: Use the documented scripts/douyin.js hot command for simple trend retrieval, and avoid or patch scripts/get-hot-trend.js unless the limit is strictly validated. <br>
Risk: The Douyin public web interface can change or apply request controls, which may cause empty, stale, or failed trend output. <br>
Mitigation: Keep request frequency modest and verify generated trend reports before using them for operational decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yezi1985201/npdouyin-hot-trend) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>
- [Douyin web interface](https://www.douyin.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands] <br>
**Output Format:** [Plain text and Markdown trend reports with optional JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Ranked items can include title, popularity value, detail link, optional cover URL, label, and content type; the documented hot command defaults to 50 items.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter and package.json report 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
