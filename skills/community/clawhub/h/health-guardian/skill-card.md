## Description: <br>
Health Guardian provides proactive health monitoring for AI agents through Apple Health export ingestion, pattern detection, and anomaly alerts for humans with chronic conditions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cgtreadw](https://clawhub.ai/user/cgtreadw) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Agents and caregivers use this skill to import Apple Health export data, maintain local health baselines, and surface anomaly alerts or summaries for people with chronic conditions or disabilities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive health telemetry and stores raw health data locally. <br>
Mitigation: Protect or encrypt the data directory and limit filesystem access before using the skill with real health exports. <br>
Risk: The configured source path may read synced Apple Health export data from iCloud-backed folders. <br>
Mitigation: Verify the exact Health Auto Export or iCloud source path and confirm which devices and accounts can access those files. <br>
Risk: Scheduled imports or caregiver alerts can continue processing and disclosing health information after setup. <br>
Mitigation: Enable cron jobs and Telegram or caregiver notifications only after confirming recipients, visibility, and a clear stop procedure. <br>
Risk: Health anomaly output may be incomplete or misleading if thresholds, baselines, or source data are wrong. <br>
Mitigation: Review configuration thresholds and treat generated alerts as decision support rather than medical advice. <br>


## Reference(s): <br>
- [Health Guardian ClawHub Release](https://clawhub.ai/cgtreadw/health-guardian) <br>
- [Health Auto Export App Store Listing](https://apps.apple.com/app/health-auto-export/id1115567069) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON files, Guidance] <br>
**Output Format:** [Markdown and plain text guidance with JSON configuration examples and shell command snippets; runtime scripts output text or Markdown alerts and summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local health data files and alert summaries based on configured thresholds and imported Apple Health export data.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
