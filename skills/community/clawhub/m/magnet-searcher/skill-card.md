## Description: <br>
Searches for movies, TV shows, or other content on magnet/torrent sites and extracts candidate magnet URLs with agent-browser. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scottzx](https://clawhub.ai/user/scottzx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to guide an agent through browser-based searches for magnet/torrent links and return candidate magnet URLs for requested content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to find magnet/torrent links for movies and similar content, which can involve copyrighted material. <br>
Mitigation: Use only for lawful, authorized content and confirm rights before searching for or using returned links. <br>
Risk: The workflow sends an agent-controlled browser to untrusted torrent-related sites. <br>
Mitigation: Use an isolated browser profile, avoid credentials or personal data, review agent-browser and Chromium sources before installation, and independently verify any result before downloading or executing files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/scottzx/magnet-searcher) <br>
- [Publisher profile](https://clawhub.ai/user/scottzx) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and extracted magnet URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include browser navigation steps, troubleshooting guidance, and candidate magnet links.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
