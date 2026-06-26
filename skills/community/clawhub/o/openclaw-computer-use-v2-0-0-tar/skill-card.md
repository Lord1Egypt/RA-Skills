## Description: <br>
Enables OpenClaw to control desktop applications, files, screenshots, screen recording, mouse and keyboard input, automation tasks, and basic system monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhmza](https://clawhub.ai/user/zhmza) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users can use this skill to let an agent operate a desktop session, including launching applications, capturing screenshots or recordings, managing files, entering keyboard input, controlling the mouse, and checking system resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad control over the active desktop session, including screenshots, recordings, clipboard access, typing, file deletion, application launching, and process termination. <br>
Mitigation: Use a separate user account, isolated desktop session, or disposable environment, and avoid machines that contain private documents, credentials, or production access. <br>
Risk: The security evidence says the skill lacks the safeguards its documentation describes. <br>
Mitigation: Review the skill before deployment and enforce confirmations, allowlists, filesystem restrictions, and logging outside the skill before enabling sensitive operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhmza/openclaw-computer-use-v2-0-0-tar) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python code examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may propose commands that affect the active desktop session and local filesystem.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
