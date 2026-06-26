## Description: <br>
Publishes Markdown articles to a Hugo blog by generating front matter, adding a summary break, updating taxonomy mapping files, and pushing changes with Git. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tanteng](https://clawhub.ai/user/tanteng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers or site operators who maintain a local Hugo blog use this skill to turn draft Markdown into a publishable post, update front matter and taxonomy files, and commit and push the changes to GitHub. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unreviewed publishing changes could write to the wrong Hugo directory or push unintended content. <br>
Mitigation: Before each push, review the target directory, Git remote, generated front matter, Markdown body, taxonomy _index.md files, and commit message. <br>
Risk: Git publishing may use credentials with broader access than this blog workflow needs. <br>
Mitigation: Prefer repository-scoped Git credentials or SSH keys limited to the blog repository. <br>


## Reference(s): <br>
- [Hugo front matter templates](references/frontmatter-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown posts, YAML front matter, taxonomy _index.md files, and Git shell commands or execution guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify Hugo content files and propose or run git add, git commit, and git push in the local blog repository.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
