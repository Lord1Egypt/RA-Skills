## Description: <br>
Searches a user's Luci-memory media and portrait data, including videos, images, recordings, transcripts, traits, events, relationships, and speeches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[memories-ai-official](https://clawhub.ai/user/memories-ai-official) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to search and retrieve grounded information from personal Luci-memory media, recordings, transcripts, and portrait data. It supports finding relevant memories, events, people, speech, images, and keyframes with filters for time, location, IDs, and people. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can search highly private personal media, recordings, transcripts, traits, relationships, and speech data. <br>
Mitigation: Install only when the user trusts memories.ai and the publisher with that data, and keep answers grounded in retrieved results. <br>
Risk: The skill supports plaintext MEMORIES_AI_KEY persistence in the skill directory. <br>
Mitigation: Prefer supplying MEMORIES_AI_KEY through a secure environment or secret manager, and rotate the key if it is exposed. <br>
Risk: Broad memory or personality questions can unintentionally trigger sensitive retrieval. <br>
Mitigation: Confirm ambiguous intent before searching and narrow retrieval by date, person, location, or media ID when possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/memories-ai-official/luci-memories) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/memories-ai-official) <br>
- [Luci-memory API host](https://skills.memories.ai/luci-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with command outputs and retrieved result lists.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MEMORIES_AI_KEY; results may include UTC timestamps, media IDs, transcripts, image bucket/blob references, locations, and similarity scores.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
