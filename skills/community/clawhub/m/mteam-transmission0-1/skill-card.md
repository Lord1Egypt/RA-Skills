## Description: <br>
A private media assistant that searches M-Team torrents and sends the user-selected item to a local Transmission downloader. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dengqijun](https://clawhub.ai/user/dengqijun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and personal media operators use this skill to search M-Team for requested films, series, or anime, review ranked torrent options, and add an explicitly selected torrent to a local Transmission/NAS workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credentials for M-Team and Transmission can be exposed or over-privileged if left in source code or broad accounts. <br>
Mitigation: Move credentials out of source code and use a limited Transmission account, as recommended by the security guidance. <br>
Risk: Incorrect NAS path mappings can send downloads to the wrong destination. <br>
Mitigation: Verify the category-to-path mapping before deployment and require the agent to show the destination before every download. <br>
Risk: The workflow adds torrents to a local downloader, which can start unwanted downloads if selection is ambiguous. <br>
Mitigation: Require explicit user selection and show the selected title, size, and destination before each download. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dengqijun/mteam-transmission0-1) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [skill.yaml](artifact/skill.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown conversation text with tool calls and setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search output lists candidate torrents by title, size, seeders, and selection number; download output reports Transmission status and NAS destination.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
