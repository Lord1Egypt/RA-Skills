## Description: <br>
Monitors GitHub organization commits daily and provides team activity updates and current standings on demand. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tenkus47](https://clawhub.ai/user/tenkus47) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and team leads use this skill to run a GitHub activity monitor that reports recent commit activity and inactive members for a configured organization team. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The monitor is hardcoded to the OpenPecha organization and team despite setup text asking for organization configuration. <br>
Mitigation: Confirm the intended organization and team before running, and edit the script if a different target is required. <br>
Risk: The script can process private-repository activity and writes local state and logs that may expose team activity data. <br>
Mitigation: Use a least-privilege read-only GitHub token, protect generated state and log files, and avoid sharing bundled or generated state data. <br>
Risk: Automated cron or channel posting can disclose activity summaries to unintended audiences. <br>
Mitigation: Enable scheduled runs and posting only after reviewing the exact output and the destination channel. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tenkus47/github-tracker) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>
- [Monitor script](artifact/scripts/monitor.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown setup guidance and plain text GitHub activity status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The monitor writes local state and log files when executed.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
