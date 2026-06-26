## Description: <br>
Draft and publish Hexo posts end-to-end with front matter, SEO polish, and deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jarxi](https://clawhub.ai/user/Jarxi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and blog maintainers use this skill to draft unpublished Hexo posts, polish existing Markdown for SEO, and publish approved updates through the Hexo deployment workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can deploy live Hexo blog updates using configured credentials. <br>
Mitigation: Require explicit approval for the target repository, changed files, and deploy intent before allowing npx hexo deploy. <br>
Risk: Removing published: false can make a draft visible on the public site. <br>
Mitigation: Keep published: false for draft-only work and confirm with the user before removing it. <br>
Risk: The skill edits Markdown and generated output inside a user-selected Hexo repository. <br>
Mitigation: Confirm the repository path before editing and review changed files before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Jarxi/hexo-blog-with-seo) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with front matter and inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update Hexo post files and propose or run Hexo clean, generate, and deploy commands after user approval.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
