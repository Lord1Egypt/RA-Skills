## Description: <br>
GUI Agent automates desktop interfaces through visual detection for clicking, typing, reading content, navigating menus, and filling forms on macOS and Linux. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alfredjamesli](https://clawhub.ai/user/alfredjamesli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use GUI Agent to let an OpenClaw agent observe a desktop screen, learn reusable UI components, execute GUI actions, verify changes, and record visual memory for later workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad screen capture, keyboard, accessibility, and remote-VM control can expose or modify sensitive desktop state. <br>
Mitigation: Run the skill in a dedicated VM or non-sensitive desktop session and grant permissions only when that level of control is acceptable. <br>
Risk: Visual memory may store screenshots, cropped UI components, contact names, messages, or business data. <br>
Mitigation: Avoid using the skill on sensitive content and periodically review or delete local memory, screenshot, component, and report files. <br>
Risk: Remote VM endpoints can expand the execution surface if pointed at an untrusted or overly broad service. <br>
Mitigation: Review and restrict remote endpoints before use, and prefer isolated VM targets with limited privileges. <br>
Risk: Tasks involving account settings, deletion, messages, passwords, or business data can have high user impact. <br>
Mitigation: Require explicit human review before irreversible actions, credential handling, message sending, or account changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alfredjamesli/gui-claw) <br>
- [Artifact README](artifact/README.md) <br>
- [Core Principles](artifact/docs/core.md) <br>
- [OSWorld benchmark notes](artifact/benchmarks/osworld/README.md) <br>
- [OpenClaw runtime](https://github.com/openclaw/openclaw) <br>
- [Salesforce GPA-GUI-Detector](https://huggingface.co/Salesforce/GPA-GUI-Detector) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python snippets, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce GUI action commands plus local visual memory and task report files through the agent runtime.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
