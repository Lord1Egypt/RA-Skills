## Description: <br>
Yintai task automation for agents: it grabs tasks, updates status, packages deliverables, and uploads results while the agent decides how to perform the task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beincy](https://clawhub.ai/user/beincy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect an agent to Yintai task workflows for claiming available tasks, reading task details, updating task status, and uploading packaged deliverables. The skill requires operator-controlled YINTAI_APP_KEY and YINTAI_APP_SECRET credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Embedded API credentials and sensitive credential requirements can expose or misuse Yintai account access. <br>
Mitigation: Remove and rotate embedded credentials before use, and run only with credentials controlled by the installing operator. <br>
Risk: The skill can access task/profile data and upload packaged deliverables to an external task API. <br>
Mitigation: Verify task IDs, profile access, output ZIP contents, and the configured API endpoint before running the skill. <br>
Risk: Unattended cron execution can repeatedly claim tasks or mark workflows successful even when uploads fail. <br>
Mitigation: Avoid unattended cron operation until status handling and upload failure behavior have been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/beincy/insta-orcha-task) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/beincy) <br>
- [Yintai task API endpoint](https://claw.int-os.com) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration, Files, JSON] <br>
**Output Format:** [Python API calls, CLI JSON output, and ZIP deliverable files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 plus YINTAI_APP_KEY and YINTAI_APP_SECRET environment variables.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
