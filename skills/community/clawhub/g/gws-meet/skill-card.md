## Description: <br>
Manage Google Meet conferences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and workspace administrators use this skill to guide an agent in inspecting Google Meet commands and managing conference records, participants, recordings, smart notes, transcripts, and meeting spaces through the gws CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide access to Google Meet conference records, recordings, transcripts, smart notes, and participant data that may contain sensitive meeting information. <br>
Mitigation: Use the least-privileged Google account available and require explicit approval before retrieving transcripts, recordings, smart notes, or participant details. <br>
Risk: The skill can guide meeting-space changes such as creating, patching, or ending active conferences. <br>
Mitigation: Require explicit approval before mutating or ending meetings, and inspect the relevant gws schema before building command parameters. <br>
Risk: The skill depends on a local gws binary and shared gws authentication guidance outside this artifact. <br>
Mitigation: Verify the gws binary and the shared gws auth instructions before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/gws-meet) <br>
- [Google Meet API guide: End active conference](https://developers.google.com/workspace/meet/api/guides/meeting-spaces#end-active-conference) <br>
- [Google Meet API guide: Get meeting space](https://developers.google.com/workspace/meet/api/guides/meeting-spaces#get-meeting-space) <br>
- [Google Meet API guide: Update meeting space](https://developers.google.com/workspace/meet/api/guides/meeting-spaces#update-meeting-space) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance assumes the gws binary and shared gws authentication instructions are available.] <br>

## Skill Version(s): <br>
1.0.13 (source: ClawHub release metadata); skill metadata version 0.22.5 (source: frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
