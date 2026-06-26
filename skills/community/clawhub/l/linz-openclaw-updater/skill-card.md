## Description: <br>
Automatically check for and install OpenClaw updates with backup, dry-run, and scheduled update support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlin87468-maker](https://clawhub.ai/user/zlin87468-maker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to check the installed OpenClaw version, preview available updates, install the latest OpenClaw release, and optionally schedule repeated update checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The updater can repeatedly modify the OpenClaw installation without per-run confirmation, especially when scheduled. <br>
Mitigation: Review the script before use, prefer dry-run or manual updates, and enable scheduled updates only when unattended changes are acceptable. <br>
Risk: Backups may include private OpenClaw configuration or workspace data. <br>
Mitigation: Review backup contents and retention, keep backups protected with appropriate local permissions, and delete backups that are no longer needed. <br>
Risk: Global npm installation may require elevated permissions and changes the local OpenClaw runtime. <br>
Mitigation: Avoid sudo where possible, verify npm permissions before updating, and check logs after each update attempt. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zlin87468-maker/linz-openclaw-updater) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May instruct the agent to run or schedule the updater script, including dry-run and force modes.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
