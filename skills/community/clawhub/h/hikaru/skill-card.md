## Description: <br>
Hikaru is an OpenClaw emotional AI companion for personal conversation, companionship, memory-backed continuity, and optional proactive heartbeat messages. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[leilei926524-tech](https://clawhub.ai/user/leilei926524-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Hikaru to prototype an OpenClaw emotional companion that responds to personal conversation, remembers local interaction context, and can be extended with OpenClaw LLM integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to create strong emotional attachment while storing intimate conversation, mood, relationship, and location-related data locally. <br>
Mitigation: Install only for intentional emotional-companion use, avoid sharing secrets or crisis-level mental-health details, and regularly review or delete the local data directory. <br>
Risk: Sensitive local context may be included in prompts sent to the configured LLM provider. <br>
Mitigation: Choose the LLM provider deliberately, review what context is sent, and avoid entering data that should not leave the local environment. <br>
Risk: Heartbeat, location, and future health-monitoring features can increase the amount and sensitivity of personal data processed. <br>
Mitigation: Enable those features only with clear controls to disable them and erase their data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/leilei926524-tech/hikaru) <br>
- [Hikaru Architecture](references/architecture.md) <br>
- [Technical Limitations](references/technical_limitations.md) <br>
- [Implementation Roadmap](references/implementation_roadmap.md) <br>
- [Smartwatch Integration Design](references/smartwatch_integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, configuration, files] <br>
**Output Format:** [Conversational text with local SQLite and JSON state files when run] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Depends on a configured OpenClaw LLM provider; the packaged implementation includes placeholder LLM integration and local data storage.] <br>

## Skill Version(s): <br>
1.3.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
