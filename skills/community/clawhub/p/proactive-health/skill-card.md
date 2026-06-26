## Description: <br>
Proactive health monitoring for AI agents. Apple Health integration, pattern detection, anomaly alerts. Built for agents caring for humans with chronic conditions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CTsolutionsdev](https://clawhub.ai/user/CTsolutionsdev) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Agents and caregivers use Health Guardian to import Apple Health exports, analyze local health readings, and surface anomaly alerts for people with chronic conditions or disabilities. Alerts and summaries are informational and require human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive Apple Health exports that may be synced through iCloud and copied into local skill data files. <br>
Mitigation: Install only after confirming the data flow is acceptable, protect local data directories, and restrict access to exported health files. <br>
Risk: Health alerts and summaries can be mistaken for medical advice or emergency monitoring. <br>
Mitigation: Treat outputs as informational, require human review, and keep appropriate clinical or emergency escalation processes outside the skill. <br>
Risk: Hourly imports, heartbeat checks, Telegram alerts, or caregiver notifications may send sensitive or misleading information if configured loosely. <br>
Mitigation: Review thresholds, recipients, schedules, and notification content before enabling automated monitoring. <br>


## Reference(s): <br>
- [Health Auto Export](https://apps.apple.com/app/health-auto-export/id1115567069) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local JSON health data files, alert summaries, and human-readable health summaries when scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
