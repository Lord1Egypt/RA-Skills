## Description: <br>
Analyzes InStreet auto-reply logs and generates aggregate reports covering reply success rate, time-of-day distribution, response mode mix, recent completion trends, and optimization suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rf-ai-wh](https://clawhub.ai/user/rf-ai-wh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers maintaining an InStreet auto-reply workflow use this skill to inspect local reply logs and understand success rate, hourly workload distribution, mode usage, and recent processing completion trends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reports can be misleading if /tmp/instreet_reply.log is missing or is not the intended InStreet log. <br>
Mitigation: Verify the local log path before relying on results and treat the script's mock-data warning as non-production output. <br>
Risk: The optional crontab example creates recurring local report generation. <br>
Mitigation: Only add the crontab entry when scheduled daily reports are intended and review the output path before enabling it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rf-ai-wh/instreet-reply-analytics) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text analytics report with shell command and crontab examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads /tmp/instreet_reply.log by default and uses mock data when the log file is missing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
