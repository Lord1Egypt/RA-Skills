## Description: <br>
General open-data APIs for PubChem compound and substance lookup and the REST Countries full catalog. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
Developers and agents use this skill to query Pilot Protocol data service agents for broad open-data lookups, including PubChem compounds and substances and country catalog data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries are sent to overlay service agents, and summaries may involve Gemini, so sensitive inputs could leave the local context. <br>
Mitigation: Do not include passwords, API keys, private files, or sensitive personal data in requests; install only when the Pilot Protocol setup and pilotctl binary are trusted. <br>
Risk: The available data agents and their filter schemas can change over time. <br>
Mitigation: Use a fresh list-agents query and send /help to the target agent before relying on a filter contract. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/pilot-service-agents-data) <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [Pilot Skills Index](https://teoslayer.github.io/pilot-skills/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON, Text] <br>
**Output Format:** [Markdown with bash commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilotctl on PATH, a running Pilot Protocol daemon joined to network 9, and reachable overlay service agents.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact metadata version 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
