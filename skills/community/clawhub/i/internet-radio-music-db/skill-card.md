## Description: <br>
Builds and manages a local internet radio music stream database from internet-radio.com, including stream collection, availability checks, statistics, exports, and adaptive bitrate-based health checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dynamicsalex](https://clawhub.ai/user/dynamicsalex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to populate, inspect, maintain, and export a local database of internet radio streams for playback workflows. It is also intended to work with companion player and WebUI skills for browser-based stream database management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts internet-radio.com and many third-party stream servers during collection and availability checks. <br>
Mitigation: Install and run it only on networks where that outbound traffic is acceptable. <br>
Risk: Frequent cron schedules and high worker counts can create substantial network activity. <br>
Mitigation: Lower worker counts or avoid frequent schedules on metered, restricted, or monitored networks. <br>
Risk: The scripts update the local stream database state. <br>
Mitigation: Review database changes or export backups before running maintenance commands that rebuild or prune streams. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dynamicsalex/internet-radio-music-db) <br>
- [Metadata homepage](https://clawhub.ai/skills/internet-radio-music-db) <br>
- [Publisher profile](https://clawhub.ai/user/dynamicsalex) <br>
- [Internet Radio source catalog](https://www.internet-radio.com/) <br>
- [Internet Radio Music WebUI companion skill](https://clawhub.ai/dynamicsAlex/internet-radio-music-webui) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; scripts update local JSON state and print command-line reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Python scripts that read and write state.json, contact internet-radio.com and stream servers, and can be scheduled with cron.] <br>

## Skill Version(s): <br>
2.6.3 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
