## Description: <br>
Operates Home Assistant through the OOMOL home_assistant connector for reading data and running approved actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect Home Assistant configuration, entity states, events, services, and templates, and to run user-confirmed service calls or events through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run Home Assistant control actions that change real devices or automations. <br>
Mitigation: Require explicit user confirmation of the exact action, target entities, payload, and expected effect before running call_service or fire_event. <br>
Risk: The skill requires a connected Home Assistant account and should be trusted with sensitive account access. <br>
Mitigation: Install only if the user trusts OOMOL, use the OOMOL connection flow, and avoid asking for or exposing raw Home Assistant tokens. <br>
Risk: Dynamic templates and broad state reads may reveal sensitive details about the connected Home Assistant instance. <br>
Mitigation: Review requested templates and read scopes before execution, and only return information relevant to the user's request. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-home-assistant) <br>
- [Home Assistant Homepage](https://www.home-assistant.io) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute oo CLI connector actions that return JSON responses with data and an execution id.] <br>

## Skill Version(s): <br>
1.0.2 (source: server evidence release and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
