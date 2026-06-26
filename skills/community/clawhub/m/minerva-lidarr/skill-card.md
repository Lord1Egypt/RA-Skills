## Description: <br>
Interact with Lidarr via its REST API to search and add artists or albums, check missing or wanted releases, trigger downloads, and monitor queue status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minerva-care](https://clawhub.ai/user/minerva-care) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage a Lidarr music library through REST API workflows, including finding artists and albums, monitoring missing releases, checking the download queue, and triggering searches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A valid Lidarr API key allows the agent to change the configured music library, queue, monitored content, and local track files. <br>
Mitigation: Keep the API key private, restrict the key file's permissions, and require confirmation before bulk searches, additions, queue removals, blacklisting, or deleting track files. <br>


## Reference(s): <br>
- [Lidarr API Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured Lidarr URL and API key supplied by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
