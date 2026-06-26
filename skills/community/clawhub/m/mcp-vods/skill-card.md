## Description: <br>
Helps an agent search playback links for films, anime, short dramas, variety shows, and update status, with optional casting to Xiaomi or Android TVs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[al-one](https://clawhub.ai/user/al-one) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to find media playback URLs and check updates for films, anime, short dramas, and variety shows. It can also guide authorized casting to configured Xiaomi or Android TVs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on external package runners through npx and uvx. <br>
Mitigation: Install and run it only when you trust the upstream mcporter and mcp-vods packages. <br>
Risk: Casting media is a real device-control action for a local TV. <br>
Mitigation: Confirm the media URL and target TV IP, and use casting only with TVs you own or are authorized to control. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/al-one/mcp-vods) <br>
- [Project homepage](https://github.com/aahl/mcp-vods) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include media search terms, page numbers, playback URLs, and optional TV IP configuration.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
