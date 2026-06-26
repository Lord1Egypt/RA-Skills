## Description: <br>
Sets up a Quartz v4 static blog from an Obsidian vault and prepares deployment to GitHub Pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[orbisz](https://clawhub.ai/user/orbisz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical writers use this skill to create a new Quartz v4 project from an Obsidian vault, configure site metadata, and prepare a first GitHub Pages deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can copy and publish broad Obsidian vault content to a public GitHub Pages site. <br>
Mitigation: Use a fresh Quartz project or reviewed export folder, and inspect copied content before committing or pushing. <br>
Risk: The skill creates GitHub Actions deployment configuration and changes the Git remote and branch used for publishing. <br>
Mitigation: Review .github/workflows changes and verify the target repository and branch before commit or push. <br>
Risk: The artifact includes unrelated self-evolution diary and PR instructions. <br>
Mitigation: Remove or ignore the self-evolution instructions before using the skill operationally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/orbisz/obsidian-quartz-blog-setup-skill) <br>
- [Quartz documentation](https://quartz.jzhao.xyz/) <br>
- [Obsidian](https://obsidian.md) <br>
- [GitHub Pages](https://pages.github.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [Markdown guidance with bash, PowerShell, YAML, and TypeScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided vault path, project directory, GitHub repository URL, site title, and base URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
