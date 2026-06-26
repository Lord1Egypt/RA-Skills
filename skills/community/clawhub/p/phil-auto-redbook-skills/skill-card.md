## Description: <br>
Creates Xiaohongshu note materials by drafting note copy, generating themed image cards, and optionally publishing the note. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phil-guo](https://clawhub.ai/user/phil-guo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content creators use this skill to turn source material into Xiaohongshu-ready titles, body text, Markdown card content, rendered 3:4 image cards, and optional platform posts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing requires a live Xiaohongshu account cookie, which can expose account access if shared or committed. <br>
Mitigation: Keep XHS_COOKIE local, never commit or share .env, and test with dry-run or private posting before normal use. <br>
Risk: Rendering untrusted Markdown or HTML in a browser can create network-exposure risk. <br>
Mitigation: Render only trusted content or block network access during rendering when content comes from untrusted sources. <br>
Risk: Unpinned dependencies may change behavior across installs. <br>
Mitigation: Pin Python and Node dependencies before relying on the skill for serious publishing workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/phil-guo/phil-auto-redbook-skills) <br>
- [Playwright](https://playwright.dev/) <br>
- [Marked](https://marked.js.org/) <br>
- [xhs API client](https://github.com/ReaJason/xhs) <br>
- [Xiaohongshu](https://www.xiaohongshu.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with generated note copy, YAML-frontmatter Markdown card content, and shell commands for rendering or publishing] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated artifacts may include cover.png and card_*.png image files when the provided render scripts are executed.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
