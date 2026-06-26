## Description: <br>
Interact with Radarr, the movie manager in the *arr media management suite, via its REST API for searching movies, checking missing or wanted titles, triggering downloads, and monitoring queue status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minerva-care](https://clawhub.ai/user/minerva-care) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and media-server administrators use this skill to work with a Radarr instance through its REST API for movie lookup, adding titles, checking wanted or missing movies, triggering searches, and monitoring the download queue. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Radarr API key can allow an agent to control the configured Radarr instance. <br>
Mitigation: Store the API key as a restricted secret, avoid including it in prompts or logs, and load it only at execution time. <br>
Risk: Radarr API access can add movies, start searches, and potentially update or remove media through documented endpoints. <br>
Mitigation: Review generated commands and request payloads before execution, especially POST, PUT, and DELETE calls. <br>
Risk: The artifact shows both a concrete credential storage path and a placeholder key-loading path. <br>
Mitigation: Set the key-loading command to the intended secret path before use. <br>


## Reference(s): <br>
- [Radarr API Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a configured Radarr URL and API key to call local Radarr REST API endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
