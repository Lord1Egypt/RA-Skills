## Description: <br>
Static code analysis tool. Detects security vulnerabilities, code smells, and complexity issues across 17 languages. All analysis runs locally; no code leaves your machine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[artvepa80](https://clawhub.ai/user/artvepa80) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to run local static analysis on project directories and review security, quality, complexity, and DevOps findings before shipping code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a third-party local CLI package. <br>
Mitigation: Install it only when you trust the hefesto-ai package and want a local code-auditing CLI. <br>
Risk: Analysis reports may include sensitive source snippets or secret findings. <br>
Mitigation: Run analysis on specific project directories and protect generated reports according to your code and secrets handling policies. <br>
Risk: The optional git hook can run on future pushes in a repository. <br>
Mitigation: Enable the hook only in repositories where you intentionally want HefestoAI checks to run before pushes. <br>


## Reference(s): <br>
- [HefestoAI site](https://hefestoai.narapallc.com) <br>
- [HefestoAI setup guide](https://hefestoai.narapallc.com/setup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and examples of text, JSON, and HTML report outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the hefesto binary; analysis runs locally against user-selected project directories.] <br>

## Skill Version(s): <br>
2.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
