## Description: <br>
Scans an agent workspace and memory logs for leaked API keys, tokens, or sensitive credentials, and guides recurring audit schedule checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shingo0620](https://clawhub.ai/user/shingo0620) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to audit local workspace and memory log files for secret-looking values and to check whether a recurring memory security audit is scheduled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner reads local workspace and memory-log files that may contain sensitive information. <br>
Mitigation: Run it only where local workspace scanning is acceptable and keep findings local; the evidence describes the skill as read-only and non-exfiltrating. <br>
Risk: Regex-based secret detection can produce false positives or miss values outside the configured patterns. <br>
Mitigation: Review each masked finding before taking action, and verify suspected secrets in the relevant provider dashboard before revocation or cleanup. <br>
Risk: The Python scanner does not automatically verify or create recurring schedules. <br>
Mitigation: Treat schedule verification as a separate cron.list check and only recommend a weekly audit when no relevant recurring job is present. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shingo0620/openclaw-memory-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and scanner findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local, masked potential-secret findings and schedule-check recommendations; it does not modify files or send data out.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
