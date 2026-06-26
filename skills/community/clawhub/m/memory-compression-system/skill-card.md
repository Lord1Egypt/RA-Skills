## Description: <br>
Integrated memory management and extreme context compression for OpenClaw. Combines memory management, compression, search, and automation in one unified skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hassffw](https://clawhub.ai/user/Hassffw) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to compress, retain, search, and monitor OpenClaw memory files with manual commands or scheduled automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer or enable script can create recurring automation that runs memory compression about every six hours. <br>
Mitigation: Review the cron job behavior and configuration before running install.sh or enable.sh, and remove the scheduled job with disable.sh or OpenClaw cron management when it is no longer wanted. <br>
Risk: The skill can read and copy OpenClaw memory, then create retained compressed files and backups. <br>
Mitigation: Confirm that the memory contents, storage paths, and retention settings are acceptable before execution; run manual or test commands first when evaluating the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Hassffw/memory-compression-system) <br>
- [SKILL.md](SKILL.md) <br>
- [README.md](README.md) <br>
- [CLAWHUB-README.md](CLAWHUB-README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local file operations, retained compressed memory files, backups, logs, status output, and optional scheduled automation.] <br>

## Skill Version(s): <br>
3.0.1 (source: ClawHub release metadata; artifact files report 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
