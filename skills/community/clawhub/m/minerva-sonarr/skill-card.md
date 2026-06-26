## Description: <br>
Interact with Sonarr (TV show manager) via its REST API. Use when searching for TV series, checking missing/wanted episodes, triggering downloads, or monitoring queue status. Part of the *arr media management suite. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minerva-care](https://clawhub.ai/user/minerva-care) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators managing a Sonarr instance use this skill to search and add TV series, inspect missing episodes, start searches, and check queue status through the Sonarr REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change a Sonarr media library and start download searches when used for state-changing workflows. <br>
Mitigation: Require explicit confirmation before adding series, triggering all-missing searches, deleting episode files, or removing queue items. <br>
Risk: Exposure of the Sonarr API key can allow unauthorized control of the Sonarr instance. <br>
Mitigation: Keep the API key private, store it with restrictive file permissions, and avoid printing or committing it. <br>


## Reference(s): <br>
- [Sonarr API Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Examples expect SONARR_URL and SONARR_KEY to be configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
