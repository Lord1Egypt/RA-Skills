## Description: <br>
将 Markdown 文章发布到 Hugo 博客，自动生成 Front Matter 并推送到远程仓库。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Personal bloggers and content-focused developers use this skill to turn Markdown drafts into Hugo posts by generating Front Matter, adding a more marker, updating taxonomy files when needed, and preparing Git commit and push steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to read local blog configuration, edit Hugo content, create taxonomy files, and commit or push to a remote Git repository without clear confirmation. <br>
Mitigation: Require explicit confirmation of the blog path, files to change, draft or publish state, and whether git push is allowed before making changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/hugo-blog-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with YAML Front Matter examples and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include proposed file paths, Hugo taxonomy metadata, commit messages, and deployment links.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
