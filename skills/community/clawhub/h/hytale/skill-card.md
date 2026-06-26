## Description: <br>
Manage and control a local Hytale dedicated server with commands to start, stop, update, and check server status using the official downloader. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NewcastleGeek](https://clawhub.ai/user/NewcastleGeek) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and server operators use this skill to manage a local Hytale dedicated server, including starting, stopping, updating, and checking its status. It assumes the user provides the official Hytale downloader and credentials in the local server directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a local credentials file for the Hytale downloader. <br>
Mitigation: Keep hytale-downloader-credentials.json private, avoid committing or syncing it, and apply restrictive file permissions to ~/hytale_server. <br>
Risk: The update flow executes a user-provided Hytale downloader binary. <br>
Mitigation: Use the official downloader source, place it intentionally in ~/hytale_server, and confirm it is the expected executable before running updates. <br>
Risk: The server runs as a background screen process on the local machine. <br>
Mitigation: Monitor the server process and use the stop command when the server should no longer be running. <br>


## Reference(s): <br>
- [Hytale Downloader](https://downloader.hytale.com/hytale-downloader.zip) <br>
- [ClawHub skill page](https://clawhub.ai/NewcastleGeek/hytale) <br>
- [Publisher profile](https://clawhub.ai/user/NewcastleGeek) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Manages local files under ~/hytale_server and a background screen session for the Hytale server process.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
