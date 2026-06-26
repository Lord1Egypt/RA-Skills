## Description: <br>
Plays internet radio streams through Foobar2000 by mapping moods to genres, selecting streams from the Internet Radio Music DB, and supporting playback controls and history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dynamicsalex](https://clawhub.ai/user/dynamicsalex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to play and control internet radio through Foobar2000 by mood or genre, using the Internet Radio Music DB as the stream source. It also supports playback status, navigation, and history review or export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts internet radio stream URLs while checking availability and starting playback. <br>
Mitigation: Use it only with trusted stream database sources and apply normal network controls for outbound streaming traffic. <br>
Risk: The skill can stop or switch the local Foobar2000 playback session. <br>
Mitigation: Install it only when OpenClaw is expected to control Foobar2000, and avoid running play or stop commands during unrelated playback. <br>
Risk: Playback history is stored locally and can be exported. <br>
Mitigation: Review state.json and exported history files before sharing them, and clear local history when stream choices should remain private. <br>
Risk: The required Internet Radio Music DB skill and optional web UI plugin are separate components. <br>
Mitigation: Review and scan those components independently before using them with this player. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dynamicsalex/internet-radio-music-player) <br>
- [Internet Radio Music WebUI Plugin](https://clawhub.ai/dynamicsAlex/internet-radio-music-webui) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [CLI text output, local JSON state, and optional CSV, HTML, or JSON history exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Controls local Foobar2000 playback and records playback history in state.json.] <br>

## Skill Version(s): <br>
2.5.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
