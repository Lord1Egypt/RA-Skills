## Description: <br>
Search GIF providers with CLI/TUI, download results, and extract stills/sheets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utromaya-code](https://clawhub.ai/user/utromaya-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agent users use this skill to find GIFs from supported providers, preview results, download selected media, and extract still images or contact sheets for review and sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires the external gifgrep binary, so agent guidance may fail or produce unusable commands if gifgrep is not installed. <br>
Mitigation: Install gifgrep using one of the documented ClawHub installation methods before relying on the workflow. <br>
Risk: Provider-specific searches may require API credentials, and missing credentials can limit GIF search behavior. <br>
Mitigation: Configure required provider environment variables such as GIPHY_API_KEY when selecting providers that require them. <br>
Risk: The security guidance recommends reviewing commands before running powerful, user-directed workflows. <br>
Mitigation: Review generated shell commands before execution, especially in sensitive repositories or accounts. <br>


## Reference(s): <br>
- [Gifgrep Homepage](https://gifgrep.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/utromaya-code/gif-search-cli) <br>
- [Publisher Profile](https://clawhub.ai/user/utromaya-code) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference gifgrep CLI output, downloaded GIF files, still PNG images, contact sheet PNG images, provider URLs, and optional provider API key environment variables.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
