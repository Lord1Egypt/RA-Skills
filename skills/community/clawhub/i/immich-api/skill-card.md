## Description: <br>
Connects agents to self-hosted Immich instances to manage photos, albums, users, search media, upload and download files, and handle jobs through the Immich REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ninjazan420](https://clawhub.ai/user/ninjazan420) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and automation maintainers use this skill to connect an agent to a self-hosted Immich instance for photo library operations, including asset uploads and downloads, album management, user queries, search, library scans, and job triggers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent access to an Immich API key can expose or modify private photo library data. <br>
Mitigation: Use a dedicated least-privilege Immich API key, avoid passing the key directly on the command line, and require explicit confirmation before uploads, deletes, shared-link creation, user management, scans, or job triggers. <br>
Risk: The album downloader may write files outside the selected output directory if an Immich server returns unsafe album or file names. <br>
Mitigation: Avoid or patch download_album.py until it sanitizes album and file names and confines writes to the selected output directory. <br>


## Reference(s): <br>
- [Immich API Endpoints Reference](references/api-endpoints.md) <br>
- [ClawHub release page](https://clawhub.ai/ninjazan420/immich-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl examples, Python script usage, and configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an Immich base URL and API key; bundled scripts may read local media files and write downloaded media files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
