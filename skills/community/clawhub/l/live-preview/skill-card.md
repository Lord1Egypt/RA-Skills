## Description: <br>
Share a live preview of a website under development via aitun tunnel, with hot-reload support so users see changes in real time as you edit. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ctz168](https://clawhub.ai/user/ctz168) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to expose an in-progress local website through an aitun tunnel so collaborators can review live changes during iterative design, debugging, or prototyping. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make a selected local preview publicly reachable through an aitun tunnel. <br>
Mitigation: Expose only the intended app or directory, avoid authenticated or sensitive environments, and stop the dev server and tunnel when the preview is complete. <br>
Risk: Remote-script install shortcuts are included for Linux, macOS, and Windows. <br>
Mitigation: Prefer the pip or uv install path and review any remote install script before running it. <br>


## Reference(s): <br>
- [Live Preview on ClawHub](https://clawhub.ai/ctz168/skills/live-preview) <br>
- [OpenClaw metadata page](https://clawhub.ai/ctz168/live-preview) <br>
- [AiTun homepage](https://aitun.cc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and preview URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include public aitun preview links, process IDs for cleanup, and framework-specific local server commands.] <br>

## Skill Version(s): <br>
1.0.6 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
