## Description: <br>
Provides OpenClaw agents with a bundled workspace memory configuration and logging helper for remembering preferences, tasks, feedback, and long-term context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[githubxiaohei](https://clawhub.ai/user/githubxiaohei) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users install this skill to add persistent memory files, task logs, feedback tracking, and preference records to an OpenClaw workspace. It is suited for agents that need continuity across sessions and configurable memory practices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled workspace rules can overwrite or materially change OpenClaw workspace behavior. <br>
Mitigation: Review and edit the bundled workspace files before installation, and back up the existing OpenClaw workspace. <br>
Risk: Memory files may persist personal profile data, identifiers, and interaction logs. <br>
Mitigation: Remove prefilled personal details, define consent and deletion rules, and avoid storing secrets or sensitive data. <br>
Risk: The configuration encourages proactive checks and autonomous actions beyond simple memory support. <br>
Mitigation: Disable proactive email, calendar, social checks, background preloading, and commit or push autonomy unless explicitly required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/githubxiaohei/openclaw-memory-fix-skill) <br>
- [Publisher profile](https://clawhub.ai/user/githubxiaohei) <br>
- [Artifact skill overview](artifact/SKILL.md) <br>
- [Artifact skill configuration](artifact/memory-fix.json) <br>
- [Artifact security settings](artifact/config-files/SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown configuration files, JSON metadata, and a shell script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Installs workspace-oriented memory files and appends dated memory log entries when the helper script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
