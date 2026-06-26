## Description: <br>
Searches across ten music sources and downloads MP3 files, automatically trying alternate sources and applying source-specific Referer handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wehaha](https://clawhub.ai/user/wehaha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents can use this skill when a user asks to find and download permitted MP3 music from supported music services. It is intended for song lookup and file retrieval workflows where network access and local writes to /tmp/music are acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Song searches are sent to multiple third-party music services. <br>
Mitigation: Use the skill only when users accept third-party music-service requests for their search terms. <br>
Risk: The downloader disables HTTPS certificate verification for requests. <br>
Mitigation: Run it only in environments where this transport-security tradeoff is acceptable, and avoid using it for sensitive searches. <br>
Risk: Downloaded MP3 files are saved under /tmp/music. <br>
Mitigation: Confirm the runtime has appropriate local storage permissions and clean up downloaded files when they are no longer needed. <br>
Risk: The skill downloads music from external services. <br>
Mitigation: Use it only for music the user is permitted to download. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wehaha/music-downloader) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Guidance] <br>
**Output Format:** [Plain text status output with a downloaded MP3 file path on success] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads MP3 files under /tmp/music by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
