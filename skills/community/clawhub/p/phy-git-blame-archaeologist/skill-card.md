## Description: <br>
Git Blame Archaeologist helps developers trace git blame and file history to explain why lines or code blocks exist, including commit context, renames, linked references, and mystery blocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to investigate why code exists by tracing local Git blame, commit history, rename history, issue references, and terse or unexplained commits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive local repository history, including diffs, commit bodies, author emails, branch history, and issue or ticket references. <br>
Mitigation: Use it only in repositories where that history may be inspected, and prefer explicit slash-command use with a specific file, line, or range in private codebases. <br>


## Reference(s): <br>
- [Canlah AI homepage](https://canlah.ai) <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-git-blame-archaeologist) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with inline shell commands and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Works offline against a local Git repository and may summarize commit metadata, diffs, authors, branches, and linked issue or ticket references.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
