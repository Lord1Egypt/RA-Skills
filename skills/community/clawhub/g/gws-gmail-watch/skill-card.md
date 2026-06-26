## Description: <br>
Gmail: Watch for new emails and stream them as NDJSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to watch Gmail mailboxes with the gws CLI, stream new messages as NDJSON, and optionally write messages as JSON files. It supports Gmail push/Pub/Sub setup or reuse for ongoing monitoring workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Watching Gmail can expose private email contents through NDJSON streams or per-message JSON files. <br>
Mitigation: Use the intended Google account and GCP project, restrict labels and message format where practical, and protect any output as private email data. <br>
Risk: Pub/Sub resources may remain after the watcher exits when cleanup is not requested. <br>
Mitigation: Use --cleanup when resources should not persist, or review existing Pub/Sub resources before reusing a topic or subscription. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/gws-gmail-watch) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash commands, flag tables, and operational notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The documented command can stream Gmail messages as NDJSON or write each message to a separate JSON file.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata; artifact metadata.version is 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
