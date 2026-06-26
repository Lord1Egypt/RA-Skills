## Description: <br>
Pixiv Skill helps agents retrieve Pixiv rankings, search artworks, cache metadata, download selected images, monitor artists, and perform like, bookmark, or follow actions using user-provided Pixiv authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[firstmeet1108](https://clawhub.ai/user/firstmeet1108) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to automate Pixiv discovery workflows, including ranking lookup, keyword search, metadata review, selective artwork download, artist monitoring, and account interactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles live Pixiv credentials and authentication material. <br>
Mitigation: Treat config.yaml as a secrets file, keep it out of source control and shared logs, and review the configuration before running commands. <br>
Risk: The skill can change a user's Pixiv account state through like, bookmark, follow, download, or monitoring commands. <br>
Mitigation: Require explicit user approval before running account-changing or long-running monitoring commands. <br>
Risk: Proxy settings can route authenticated Pixiv traffic through an untrusted network path. <br>
Mitigation: Use only trusted proxies and leave the proxy setting empty when one is not required. <br>


## Reference(s): <br>
- [Pixiv](https://www.pixiv.net/) <br>
- [Pixiv ranking endpoint](https://www.pixiv.net/ranking.php) <br>
- [Pixiv artwork pages](https://www.pixiv.net/artworks/{illust_id}) <br>
- [ClawHub skill page](https://clawhub.ai/firstmeet1108/pixiv) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code, files] <br>
**Output Format:** [Markdown guidance with shell commands, YAML configuration, JSON metadata, and downloaded image files when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include cached artwork metadata, Pixiv artwork URLs, local image files, and status text from Pixiv API calls.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
