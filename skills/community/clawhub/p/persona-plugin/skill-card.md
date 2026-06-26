## Description: <br>
Provides persona tools for retrieving persistent caller context, logging completed calls, and updating caller identity, communication style, and memory records through a Persona API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noahvandal](https://clawhub.ai/user/noahvandal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents handling ClawdTalk calls use this plugin to load caller context before outreach, log call metadata after conversations, and persist new caller facts or memories for future personalization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent caller profiling can store sensitive caller identity, personality, memory, and call-summary information. <br>
Mitigation: Deploy only when persistent caller memory is intentional, callers receive appropriate notice and consent, and retention plus review, correction, and deletion processes are defined. <br>
Risk: Providing a call ID may allow full transcript ingestion by the Persona API server. <br>
Mitigation: Pass call IDs only when full transcript ingestion is acceptable for the use case and the configured Persona API server is trusted. <br>
Risk: The plugin depends on an external Persona API server and API key. <br>
Mitigation: Protect the API key, configure a trusted server endpoint, and allow calls to proceed without persona context when the API is unreachable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/noahvandal/persona-plugin) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, API calls, configuration, guidance] <br>
**Output Format:** [JSON tool results and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Persona API key and server URL; tools may return caller profiles, prompt context, recent call history, call records, and persona document version metadata.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
