## Description: <br>
Search song lyrics by title and artist using the LrcApi public API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hone1983](https://clawhub.ai/user/hone1983) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to look up song lyrics by title and optional artist, then display or print cleaned plain-text lyrics from LRC responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Song titles and artist names are sent to the public LrcApi service. <br>
Mitigation: Use only the title and artist needed for the lyrics lookup, and avoid adding unrelated private information to search terms. <br>
Risk: The public lyrics API may be slow or return no result for a particular query. <br>
Mitigation: Use a reasonable timeout and retry with title-only or alternate song-name spellings when appropriate. <br>


## Reference(s): <br>
- [Lyrics Search on ClawHub](https://clawhub.ai/hone1983/lyrics-search) <br>
- [LrcApi lyrics endpoint](https://api.lrc.cx/lyrics?title={title}&artist={artist}) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, Markdown, Guidance] <br>
**Output Format:** [Markdown or plain text lyrics, optionally transformed from LRC timestamped text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include song title, artist, and credits header for printable output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
