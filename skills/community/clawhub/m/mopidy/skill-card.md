## Description: <br>
Control a Mopidy music system via Mopidy JSON-RPC for everyday listening, queue management, and playback control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[grantmacnamara](https://clawhub.ai/user/grantmacnamara) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People who operate a Mopidy music system use this skill to inspect playback, search local libraries, manage queues and playlists, and control playback through JSON-RPC. It also helps match ranked or canonical music requests against locally available tracks before queueing them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change playback state or clear the queue. <br>
Mitigation: Confirm destructive queue actions and default to adding to the queue unless the user explicitly asks to clear or play immediately. <br>
Risk: MOPIDY_URL directs the agent to a network service that can receive control requests. <br>
Mitigation: Set MOPIDY_URL only to a Mopidy endpoint the user controls. <br>
Risk: Ranked or canonical requests may use external web searches that disclose music preferences or query text. <br>
Mitigation: Tell the agent to use only the local library when external ranking lookups are not desired, and report unmatched items instead of substituting. <br>


## Reference(s): <br>
- [Mopidy API Notes](references/api-notes.md) <br>
- [ClawHub skill page](https://clawhub.ai/grantmacnamara/mopidy) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown text with shell commands and JSON-RPC responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, python3, and MOPIDY_URL; ranked music requests may use external web search before matching results against the local library.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
