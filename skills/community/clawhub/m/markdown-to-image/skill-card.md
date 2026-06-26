## Description: <br>
Converts Markdown files or inline Markdown into paginated image cards for sharing on social platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reffwu](https://clawhub.ai/user/reffwu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content creators use this skill to turn Markdown documents into polished multi-image card sets for WeChat, Xiaohongshu, Weibo, and similar social platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The renderer can silently delete the selected output folder. <br>
Mitigation: Use the default Downloads output location or choose an empty disposable output directory before generation. <br>
Risk: Rendering Markdown can make outbound network requests for remote images or fonts. <br>
Mitigation: Process trusted Markdown, remove remote image links for sensitive files, or run with network access restricted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/reffwu/markdown-to-image) <br>
- [README.md](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands that produce PNG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated images are written under ~/Downloads/<card name>/ by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
