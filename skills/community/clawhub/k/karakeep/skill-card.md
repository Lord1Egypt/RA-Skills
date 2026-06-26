## Description: <br>
Manage bookmarks and links in a Karakeep instance by saving links, listing recent bookmarks, and searching a collection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jayphen](https://clawhub.ai/user/Jayphen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to manage bookmarks in their own Karakeep instance: configure credentials, save links or text, list recent bookmarks, and search their collection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Karakeep API keys may be stored locally in plaintext when the login command writes ~/.config/karakeep/config.json. <br>
Mitigation: Prefer environment variables or a protected credential store when available, and restrict permissions on ~/.config/karakeep/config.json if file-based storage is used. <br>
Risk: The skill sends requests to the configured Karakeep instance URL using bearer-token authentication. <br>
Mitigation: Confirm the instance URL is trusted before configuring credentials. <br>


## Reference(s): <br>
- [Karakeep skill page](https://clawhub.ai/Jayphen/karakeep) <br>
- [Jayphen publisher profile](https://clawhub.ai/user/Jayphen) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI output text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses uv with the requests package and reads the Karakeep URL and API key from environment variables or ~/.config/karakeep/config.json.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
