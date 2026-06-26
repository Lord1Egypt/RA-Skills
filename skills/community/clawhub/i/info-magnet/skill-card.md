## Description: <br>
Info Magnet - set up topics you care about and let information come to you, with support for web search, RSS feeds, URL monitoring, and periodic scans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[besty0121](https://clawhub.ai/user/besty0121) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Info Magnet to configure topic, RSS, and URL monitors that surface new relevant content without repeated manual searches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private URLs, internal services, sensitive research topics, feed URLs, seen URLs, and digests may be stored locally when agents run scans. <br>
Mitigation: Install only when local storage under ~/.openclaw/memory is acceptable, avoid sensitive targets, and review any scheduled heartbeat scans or shared home-directory sync before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/besty0121/info-magnet) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions, CLI text output, and local JSON digest files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores monitored topics, feed URLs, seen URLs, and digests locally under ~/.openclaw/memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
