## Description: <br>
Monitor Strait of Hormuz shipping traffic from JMIC, Iranian sources, and news aggregation, write findings to MONITOR_LOG.md, and auto-update website data after each cycle. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xingpt88](https://clawhub.ai/user/xingpt88) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts and operators use this skill to collect current Strait of Hormuz maritime, geopolitical, and market signals, append a structured monitoring entry, and publish updated website data after each cycle. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local deployment script that can push data to GitHub and trigger a public website update. <br>
Mitigation: Inspect ~/hormuz-website/scripts/update_and_deploy.sh before use, confirm the target repository and branch, and run it only with credentials scoped to the intended site. <br>
Risk: The workflow trims MONITOR_LOG.md entries older than 7 days. <br>
Mitigation: Keep a separate backup or archive of MONITOR_LOG.md if older monitoring history must be retained. <br>


## Reference(s): <br>
- [JMIC Products](https://www.ukmto.org/partner-products/jmic-products) <br>
- [Windward Maritime Intelligence Blog](https://windward.ai/blog/) <br>
- [Tasnim News English](https://www.tasnimnews.ir/en/) <br>
- [Fars News English](https://www.farsnews.ir/en) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Markdown monitoring log entries with concise text summaries and an optional alert summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Updates MONITOR_LOG.md, trims entries older than 7 days, and may run a local deployment script after each monitoring cycle.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
