## Description: <br>
LocalMiniDrama短剧助手 lets an agent control a LocalMiniDrama backend through natural language to create scripts, characters, scenes, props, storyboards, images, videos, completed episodes, and project imports or exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuanyustudio](https://clawhub.ai/user/xuanyustudio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators and developers use this skill to operate LocalMiniDrama projects from an agent chat, including project creation, script and asset generation, storyboard management, media generation, video composition, and import/export workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send scripts, media, and API keys to the configured LocalMiniDrama backend. <br>
Mitigation: Use only localhost or controlled infrastructure, and install the skill only when the configured backend is trusted. <br>
Risk: Delete, import/export, bulk generation, and API-key update actions can materially change projects or expose private content. <br>
Mitigation: Require manual confirmation before allowing the agent to execute those actions. <br>
Risk: Public tunnels can expose private content or credentials when connecting to a local backend. <br>
Mitigation: Avoid public tunnels for private projects or keys unless the operator has reviewed and accepted the exposure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xuanyustudio/local-mini-drama) <br>
- [LocalMiniDrama project homepage](https://github.com/xuanyustudio/LocalMiniDrama) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration, Shell commands, Markdown] <br>
**Output Format:** [Markdown guidance with HTTP API actions and configuration commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include LocalMiniDrama project identifiers, task polling instructions, generated-content workflow steps, and import/export actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact files report 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
