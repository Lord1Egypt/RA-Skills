## Description: <br>
Cron Scheduler helps inspect cron and systemd timer tasks, view a user's crontab, and report recent failure-related log lines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingaiwork](https://clawhub.ai/user/kingaiwork) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to inspect scheduled tasks and gather cron or systemd timer status while troubleshooting automation. It can also surface recent failure-related log lines when run on a host that exposes the relevant local logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool can display local crontab entries and read local system logs when run on a host. <br>
Mitigation: Run it only in environments where the executing user is permitted to inspect scheduled tasks and local logs. <br>
Risk: The metadata includes unrelated financial referral links. <br>
Mitigation: Treat those links as unrelated to the cron utility and do not rely on them for installation, support, or security decisions. <br>
Risk: The advertised visual scheduler, pause/resume controls, and add/log commands are not supported by the current code evidence. <br>
Mitigation: Use the implemented flags such as --list, --crontab, --failures, --pro, and --version, and verify behavior before depending on claimed management features. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kingaiwork/king-cron-scheduler) <br>
- [Publisher profile](https://clawhub.ai/user/kingaiwork) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and command examples; JSON when the Python entrypoint is executed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The entrypoint reads local cron, systemd timer, and syslog data available to the executing user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
