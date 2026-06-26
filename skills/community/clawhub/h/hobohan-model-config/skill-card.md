## Description: <br>
Configure and troubleshoot OpenClaw model providers, routing, session model locks, cron model pinning, and provider switching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hohobohan](https://clawhub.ai/user/hohobohan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure OpenClaw model providers, confirm active session models, pin cron models, and troubleshoot provider routing issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide an agent through provider settings and API key handling. <br>
Mitigation: Use it only where the agent is allowed to inspect or edit OpenClaw configuration and handle provider credentials. <br>
Risk: Model configuration changes can leave existing sessions or scheduled jobs using an unexpected model. <br>
Mitigation: Confirm the active model after changes, use explicit session switching when needed, and pin models for time-sensitive cron jobs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hohobohan/hobohan-model-config) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, code] <br>
**Output Format:** [Markdown with inline JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide inspection or edits of OpenClaw provider configuration, cron payloads, and session model settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and changelog, released 2026-06-03) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
