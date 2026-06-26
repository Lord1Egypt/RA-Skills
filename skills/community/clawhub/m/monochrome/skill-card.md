## Description: <br>
Browse and search music from monochrome.tf (Tidal-based Hi-Fi streaming), including artists, albums, tracks, lyrics, recommendations, and streaming URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ricanwarfare](https://clawhub.ai/user/ricanwarfare) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search music catalogs and retrieve track metadata, lyrics, recommendations, and stream URLs for music discovery and playback workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Music searches, track identifiers, and stream requests are sent to external Monochrome or Hi-Fi API instances. <br>
Mitigation: Use the primary instance when possible and avoid community endpoints that are not trusted for the user's workflow. <br>
Risk: Returned stream URLs may involve copyright, licensing, or service-term obligations. <br>
Mitigation: Use streams only in compliance with applicable copyright rules and service terms. <br>
Risk: Bulk or repeated API usage may hit service rate limits. <br>
Mitigation: Apply reasonable delays and retry behavior for batch searches or repeated metadata requests. <br>


## Reference(s): <br>
- [Monochrome Web](https://monochrome.tf) <br>
- [Primary Monochrome Hi-Fi API](https://eu-central.monochrome.tf) <br>
- [Monochrome API Status](https://tidal-uptime.jiffy-puffs-1j.workers.dev) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Guidance, Markdown] <br>
**Output Format:** [Markdown with API endpoint examples and inline curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to call external Monochrome or Hi-Fi API instances that return JSON metadata and stream URLs.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
