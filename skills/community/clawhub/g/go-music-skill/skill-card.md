## Description: <br>
Search songs, download playable audio, fetch lyrics, parse music share links, configure platform cookies, and switch music sources through a local go-music-api backend on Linux, macOS, and Windows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scavin](https://clawhub.ai/user/scavin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to install and operate a local music backend, search for tracks, download playable audio files, fetch lyrics, and configure account cookies when platform restrictions require them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may request music-platform account cookies, which should be treated like sensitive credentials. <br>
Mitigation: Avoid providing real cookies unless necessary, use temporary values where possible, do not print full cookie values, and remove backend state when finished. <br>
Risk: The installer downloads and runs a persistent local backend service. <br>
Mitigation: Install only after reviewing the skill and trusting the upstream go-music-api release channel; inspect ~/.openclaw/music/log.txt and remove the runtime files when no longer needed. <br>


## Reference(s): <br>
- [Music Skill on ClawHub](https://clawhub.ai/scavin/go-music-skill) <br>
- [Cookie Configuration](docs/cookies.md) <br>
- [Windows Workflow](docs/windows.md) <br>
- [go-music-api release endpoint used by installer](https://api.github.com/repos/guohuiyuan/go-music-api/releases/latest) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Files, API Calls, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated local audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create runtime files under ~/.openclaw/music and downloaded media under ~/.openclaw/media.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
