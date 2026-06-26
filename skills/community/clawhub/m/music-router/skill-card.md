## Description: <br>
MusicRouter converts music sharing links across Chinese and major international music platforms, extracts song details and album artwork, and returns platform-specific links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leo7723](https://clawhub.ai/user/leo7723) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to help music listeners convert a shared track URL into links for preferred streaming platforms, with song metadata and album artwork for presentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted links may be fetched even when they are not normal public music links, including unexpected or internal URLs. <br>
Mitigation: Use only public music links from supported services and validate exact hostnames before executing the converter. <br>
Risk: Submitted music links are sent to third-party music and aggregation services with limited privacy disclosure. <br>
Mitigation: Avoid private or sensitive URLs, strip unnecessary query parameters, and disclose calls to Song.link, Netease, QQ Music, and other providers. <br>
Risk: Optional logging can record conversion details locally. <br>
Mitigation: Keep logging disabled unless needed for debugging and review any generated log file before sharing the workspace. <br>


## Reference(s): <br>
- [MusicRouter ClawHub Skill Page](https://clawhub.ai/leo7723/music-router) <br>
- [leo7723 ClawHub Publisher Profile](https://clawhub.ai/user/leo7723) <br>
- [Song.link](https://song.link) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands] <br>
**Output Format:** [JSON from the converter script and Markdown links for agent responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include album artwork URL, detected song information, per-platform music links, a Song.link aggregation page, and an optional local log path when logging is enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
