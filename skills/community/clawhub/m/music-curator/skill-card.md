## Description: <br>
Curates personalized playlists and music recommendations with strict intent preservation for playlists, queues, recommendation sets, artist or track expansion, and music discovery with version constraints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neqq3](https://clawhub.ai/user/neqq3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to classify music requests, preserve strict intent boundaries, curate playlists or recommendation sets, and coordinate music discovery or playback tools without substituting off-brief tracks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Music preferences and playback intent may be used when the skill coordinates with music discovery or playback tools. <br>
Mitigation: Use it only for requested music curation tasks and review candidate lists before queueing when confidence is medium or low. <br>
Risk: Ambiguous requests can lead to off-brief recommendations, such as similarity matches presented as official songs. <br>
Mitigation: Classify each request as strict identity, similarity, or hybrid, and ask a focused clarifying question when the boundary is unclear. <br>


## Reference(s): <br>
- [Music Curator ClawHub page](https://clawhub.ai/neqq3/music-curator) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown] <br>
**Output Format:** [Markdown guidance with concise track lists and queue-building instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce candidate track lists, exclusion notes, and short progress updates before or during playback requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
