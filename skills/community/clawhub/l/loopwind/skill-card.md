## Description: <br>
Generate images and videos from React + Tailwind CSS templates using the loopwind CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomtev](https://clawhub.ai/user/tomtev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to create Loopwind React and Tailwind templates, configure projects, and render image or video assets from those templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup uses an unpinned remote installer with local shell privileges. <br>
Mitigation: Review the installer before execution and pin to a known release or checksum when available. <br>
Risk: Rendering third-party templates or remote image/font URLs can execute or fetch untrusted content in the local workspace. <br>
Mitigation: Render untrusted templates and external inputs in a sandboxed workspace. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tomtev/loopwind) <br>
- [Loopwind Skill Source](https://loopwind.dev/skill.md) <br>
- [Loopwind Installer](https://loopwind.dev/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSX/TSX examples, JSON configuration, and shell command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide an agent to create .loopwind template files and invoke loopwind commands to render PNG, JPEG, SVG, GIF, or MP4 outputs.] <br>

## Skill Version(s): <br>
0.25.11 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
