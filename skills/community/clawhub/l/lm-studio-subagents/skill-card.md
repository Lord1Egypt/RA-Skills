## Description: <br>
Helps agents reduce paid API usage by discovering local LM Studio models and offloading suitable summarization, extraction, classification, rewriting, review, brainstorming, and privacy-sensitive tasks to them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[t-sinclair2500](https://clawhub.ai/user/t-sinclair2500) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to route suitable tasks to a local LM Studio server, selecting models by availability and capability while keeping processing local when quality suffices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts to the configured LM Studio API endpoint, so a non-local or untrusted endpoint could receive private task content. <br>
Mitigation: Confirm the API URL is localhost or another trusted endpoint before using the skill with private documents. <br>
Risk: Stateful mode and request logging can retain task context or full prompt and response data locally. <br>
Mitigation: Use stateful mode and --log only when needed, avoid unnecessary sensitive inputs, and review or delete local logs after use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/t-sinclair2500/lm-studio-subagents) <br>
- [LM Studio](https://lmstudio.ai) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON responses from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include response_id, model_instance_id, token usage, and optional local logs when helper scripts are used.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
