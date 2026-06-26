## Description: <br>
Music metadata and lyrics - iTunes search and Lyrics.ovh. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
Developers and agents use this skill to discover Pilot Protocol music service agents, search iTunes metadata, and request lyrics by artist and title through Lyrics.ovh. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, lyrics requests, and summary prompts are sent through Pilot Protocol agents and may involve external network services. <br>
Mitigation: Use only non-sensitive queries and avoid sending private text through the overlay or Gemini summary path. <br>
Risk: Lyrics availability and rights are upstream-dependent and not guaranteed by the skill. <br>
Mitigation: Treat lyrics results as best-effort lookup data and verify usage rights before redistribution or commercial use. <br>
Risk: The skill depends on a local pilotctl setup and network 9 service-agent availability. <br>
Mitigation: Install only in trusted Pilot Protocol environments and verify the daemon, network join, and discovered agent contracts before use. <br>


## Reference(s): <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/pilot-service-agents-music) <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, json, text] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilotctl, Pilot Protocol core skills, a running daemon joined to network 9, and reachable service agents.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
