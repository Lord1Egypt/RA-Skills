## Description: <br>
Automatically accesses the Jinri Toutiao homepage via browser automation, inputs keywords into the search bar, and collects related keyword suggestions from the auto-suggest dropdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
SEO researchers, content strategists, and market researchers use this skill to collect Jinri Toutiao search suggestions for keyword research, topic discovery, competitor analysis, and trend analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-entered keywords are sent to Toutiao through an automated browser session. <br>
Mitigation: Avoid entering secrets, private names, proprietary research terms, or sensitive topics. <br>
Risk: Frequent automated searches may trigger Toutiao anti-scraping controls or produce unreliable results. <br>
Mitigation: Use slow typing, wait between collections, and avoid high-frequency batch requests. <br>
Risk: Toutiao page structure can change, which may prevent the skill from finding the search box or suggestion list. <br>
Mitigation: Use live page snapshots to locate current elements and retry after refresh when elements are missing. <br>


## Reference(s): <br>
- [Browser Automation Best Practices](references/browser-automation-best-practices.md) <br>
- [Jinri Toutiao Page Structure Description](references/toutiao-structure.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown list of the input keyword and numbered search suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a summary report when collecting suggestions for multiple keywords.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
