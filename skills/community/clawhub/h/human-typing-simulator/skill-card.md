## Description: <br>
HumanTyping generates and plays human-like browser keystroke scripts with adjacent-key typos, corrections, thinking pauses, variable speed, optional French accent handling, and reproducible seeds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luke2day](https://clawhub.ai/user/luke2day) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to generate, preview, save, or replay realistic typing into an OpenClaw-managed browser field for controlled browser automation, demos, and form-entry testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enter text into live browser pages, including sensitive or irreversible forms. <br>
Mitigation: Use --dry-run first, verify the active tab and CSS selector, and avoid sensitive or irreversible forms unless the target has been checked carefully. <br>
Risk: Saved JSON scripts can contain private text supplied by the user. <br>
Mitigation: Treat saved script files as sensitive and avoid sharing or retaining them unnecessarily. <br>
Risk: A wrong active tab or selector can direct keystrokes to an unintended browser field. <br>
Mitigation: Start, navigate, and inspect with OpenClaw, pass an explicit --selector, and verify the page state after execution. <br>


## Reference(s): <br>
- [HumanTyping on ClawHub](https://clawhub.ai/luke2day/human-typing-simulator) <br>
- [luke2day ClawHub Publisher Profile](https://clawhub.ai/user/luke2day) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON keystroke event scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can type directly into a browser through CDP, print a dry-run preview, or save and replay JSON event scripts.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter and package.json declare 2.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
