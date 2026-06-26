## Description: <br>
Controls the local Morfeo UGC Engine to generate, manage, review, and draft social video runs for Argentine brands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PauldeLavallaz](https://clawhub.ai/user/PauldeLavallaz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Operators use this skill from OpenClaw or Telegram to create UGC video pipeline runs, inspect status and logs, advance manual review stages, select shots, and create social-media publishing drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact contains an embedded admin API credential. <br>
Mitigation: Remove and rotate the token, then provide credentials through an environment variable or secret store before installation. <br>
Risk: The skill can change engine state, advance workflow stages, create social-media drafts, read logs, and restart the local Morfeo service. <br>
Mitigation: Limit use to trusted operators and review requested actions before executing commands that mutate runs, publish drafts, or manage the service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PauldeLavallaz/morfeo-ugc-engine) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, API request examples, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger local API calls that mutate video workflow state, read logs, restart the Morfeo service, or create social-media drafts when followed by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
