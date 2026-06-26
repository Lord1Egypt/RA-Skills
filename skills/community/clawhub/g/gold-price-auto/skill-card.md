## Description: <br>
Automatically queries domestic and international gold prices hourly and reports current price matches from a public gold-price page. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hongjiahao371-pixel](https://clawhub.ai/user/hongjiahao371-pixel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run or schedule a gold-price report that fetches a public price page and prints matched gold price values. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an adjacent playwright-scraper-skill and a public website that may be unavailable, untrusted, or structurally changed. <br>
Mitigation: Confirm the dependency is installed and trusted before use, and verify reported prices against the source page when accuracy matters. <br>
Risk: Enabling the documented cron entry creates recurring hourly network requests and recurring reports. <br>
Mitigation: Enable the schedule only when hourly reporting is intended, and remove the cron entry when automation should stop. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hongjiahao371-pixel/gold-price-auto) <br>
- [Gold price data source](http://www.huangjinjiage.cn/jinrijinjia.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration instructions] <br>
**Output Format:** [Plain text console output with optional cron command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prints up to 20 matched price values and the cited data source.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
