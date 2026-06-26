## Description: <br>
Syncs the Kilocode provider model list in openclaw.json with the live Kilo AI API, but this release is deprecated because Kilocode Gateway is now built into OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guillaumemaka](https://clawhub.ai/user/guillaumemaka) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators who still maintain the deprecated Kilocode sync workflow use this skill to compare Kilo AI model data with OpenClaw configuration, prepare patches, and report results for approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The deprecated workflow can change OpenClaw configuration and restart the gateway after loosely scoped approval signals. <br>
Mitigation: Inspect the generated diff and patch before applying, confirm the approval came from the intended person and session, and rely on the backup created before configuration changes. <br>
Risk: The workflow reads KILOCODE_API_KEY, sends Telegram updates, and writes persistent operational notes. <br>
Mitigation: Run it only in a trusted maintenance environment, keep the API key scoped to the intended account, and avoid including sensitive model or operational details in notifications. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/guillaumemaka/kilocode-model-sync) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON status objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create snapshots, diffs, patch JSON files, operational notes, and configuration updates when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
