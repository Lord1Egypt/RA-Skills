## Description: <br>
Lyric Sense helps an agent search for song lyrics by artist and title, display timestamped LRC lyrics, fetch cover art, and optionally use a bundled local LrcApi service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adminlove520](https://clawhub.ai/user/adminlove520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve and present lyrics for a requested song, with optional local deployment of LrcApi for self-hosted lyric and cover lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Song and artist searches may be sent to third-party lyric and cover services. <br>
Mitigation: Use the static viewer only when sharing those search terms with third-party services is acceptable, or deploy a reviewed local service instead. <br>
Risk: The bundled LrcApi server has broad file, database, network, and metadata-changing capabilities. <br>
Mitigation: Do not expose the local API publicly; run it with authentication, minimal filesystem access, and isolation from sensitive music or host directories. <br>
Risk: Build scripts and metadata/file-management APIs can alter local files or service state. <br>
Mitigation: Avoid those paths unless they have been reviewed and executed in a controlled environment. <br>


## Reference(s): <br>
- [Lyric Sense ClawHub page](https://clawhub.ai/adminlove520/lyric-sense) <br>
- [adminlove520 publisher profile](https://clawhub.ai/user/adminlove520) <br>
- [LyricSense demo](https://adminlove520.github.io/lyric-sense) <br>
- [LrcApi documentation](https://docs.lrc.cx/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with API URLs, shell commands, and lyric text snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include timestamped LRC lyric lines and setup instructions for public or local API use.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
