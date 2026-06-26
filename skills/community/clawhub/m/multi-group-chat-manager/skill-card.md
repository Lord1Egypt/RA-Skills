## Description: <br>
Multi Group Chat Manager helps an OpenClaw agent manage multiple group chats by collecting messages, maintaining local user profiles and affection scores, applying rule-based scoring, and tracking online/offline chat sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pppig1357](https://clawhub.ai/user/pppig1357) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Group administrators and agent developers use this skill to configure an OpenClaw assistant that records group-chat activity, builds local user profiles, applies group-specific affection rules, and summarizes state for follow-up interactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can collect group-chat history and build lasting local user profiles and scores. <br>
Mitigation: Use it only for groups you administer, give members clear notice, and configure only the intended groups. <br>
Risk: Generated profile, affection, session, rule, and log files may contain sensitive behavioral data. <br>
Mitigation: Restrict filesystem access to generated data and define retention, deletion, and authorization controls before operational use. <br>
Risk: An exposed OneBot endpoint could allow unintended message access or control. <br>
Mitigation: Keep the OneBot endpoint bound to localhost or otherwise protect it with network and access controls. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/pppig1357/multi-group-chat-manager) <br>
- [Publisher profile](https://clawhub.ai/user/pppig1357) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration, and Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local JSON-backed profile, affection, session, rule, and log files when its scripts are run.] <br>

## Skill Version(s): <br>
1.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
