## Description: <br>
OpenClaw Dual Cleanup helps agents preview and run OpenClaw session, cache, and physical file cleanup to address stale session files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ltap266](https://clawhub.ai/user/ltap266) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inspect, preview, and run cleanup of stale OpenClaw session indexes, physical session files, and cache files across Windows, macOS, and Linux. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The cleanup behavior can delete local OpenClaw session and cache files using broad matching. <br>
Mitigation: Run dry-run mode first, review the exact files selected for deletion, and keep backups for data that must be retained. <br>
Risk: Force mode and scheduled automation can remove files without interactive confirmation. <br>
Mitigation: Avoid force mode and cron/startup/heartbeat automation until the deletion scope has been validated in the target environment. <br>
Risk: Running with elevated privileges can expand the deletion impact beyond the normal user workspace. <br>
Mitigation: Run as the normal user and avoid sudo or Administrator privileges unless there is a specific, reviewed need. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ltap266/openclaw-dual-cleanup) <br>
- [Publisher profile](https://clawhub.ai/user/ltap266) <br>
- [README.md](README.md) <br>
- [Test usage guide](test-usage.md) <br>
- [CHANGELOG.md](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and console output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include dry-run previews, cleanup reports, and configuration guidance for scheduled cleanup.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
