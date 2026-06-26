## Description: <br>
Read and write flomo memos on macOS, including recent memo retrieval, local cache search, and new memo creation through an incoming webhook or URL scheme. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DoTheWorkNow](https://clawhub.ai/user/DoTheWorkNow) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent retrieve, search, tag-filter, summarize, and create Flomo memos on a macOS system where the Flomo desktop app is installed and logged in. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read private Flomo memos using the local Flomo desktop login state. <br>
Mitigation: Install and run it only in trusted agent environments, and avoid sharing local Flomo configuration or access tokens. <br>
Risk: The skill can create new Flomo memos through a webhook or URL scheme. <br>
Mitigation: Review memo write and verification commands before execution, especially when an agent proposes content to write. <br>
Risk: Changing FLOMO_API_BASE or webhook settings can send requests or memo content to a non-Flomo destination. <br>
Mitigation: Keep API base and webhook settings pointed at trusted Flomo endpoints unless a reviewer has explicitly approved the override. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/DoTheWorkNow/openclaw-flomo-skill) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Flomo API base](https://flomoapp.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command output may include memo content, tags, timestamps, webhook write status, and verification check results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
