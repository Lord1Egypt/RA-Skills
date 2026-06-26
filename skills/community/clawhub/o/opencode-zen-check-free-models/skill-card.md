## Description: <br>
Monitors the OpenCode Zen pricing page for new free models and offers to update your default configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pranjal-joshi](https://clawhub.ai/user/pranjal-joshi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to monitor OpenCode Zen pricing for newly available free models and decide whether to update local default model configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches a public pricing page with curl, so it depends on current remote page availability and content. <br>
Mitigation: Install only if remote pricing-page access is acceptable, and review detected model IDs before changing defaults. <br>
Risk: The skill writes ./zen_seen_models.json in the current workspace and can offer to change local OpenClaw defaults. <br>
Mitigation: Allow configuration changes only after user confirmation and review local workspace changes after execution. <br>


## Reference(s): <br>
- [OpenCode Zen pricing documentation](https://opencode.ai/docs/zen/#pricing) <br>
- [ClawHub skill page](https://clawhub.ai/pranjal-joshi/opencode-zen-check-free-models) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, JSON files] <br>
**Output Format:** [Markdown guidance with shell commands and local JSON/configuration updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create ./zen_seen_models.json and may update local OpenClaw defaults after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
