## Description: <br>
Track laundry loads, view usage stats, and export reports in multiple formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to log laundry activity, review laundry history and usage patterns, manage reminders and checklists, and export locally stored records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Laundry schedules, costs, reminders, and free-form notes are saved locally and may persist on shared or backup-synced machines. <br>
Mitigation: Avoid entering highly sensitive notes, and delete ~/.local/share/laundry/ or generated exports when the records are no longer needed. <br>
Risk: Exported JSON, CSV, or text reports can expose user-entered laundry records if shared or left in the data directory. <br>
Mitigation: Review exported files before sharing and remove exports after use. <br>


## Reference(s): <br>
- [Laundry ClawHub page](https://clawhub.ai/ckchzh/laundry) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; local JSON, CSV, or text exports when the CLI is run] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores and exports user-entered laundry records under ~/.local/share/laundry/.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
