## Description: <br>
Manage Overleaf LaTeX projects via git integration or native agent tools for cloning, branching, compiling, pushing, status checks, and health checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wahajahmed010](https://clawhub.ai/user/wahajahmed010) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document authors use this skill to manage Overleaf LaTeX projects through git, compile documents locally, and push verified changes back to Overleaf. It is especially suited to resume versioning workflows that need branch-per-target variants. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow requires Overleaf credentials and may involve sensitive account access. <br>
Mitigation: Use a revocable Overleaf token where possible, keep the credential file private, and maintain restrictive file permissions. <br>
Risk: Global plaintext git credential storage can expose Overleaf credentials if the local environment is compromised. <br>
Mitigation: Consider a more secure git credential helper than global plaintext storage. <br>
Risk: Commits, pushes, merges, and branch deletions can alter or remove Overleaf project work. <br>
Mitigation: Review local compilation results and confirm git operations before executing them. <br>
Risk: The skill references a separate Overleaf plugin that is outside the core skill workflow. <br>
Mitigation: Review the separate plugin before installation or use. <br>


## Reference(s): <br>
- [Overleaf LaTeX on ClawHub](https://clawhub.ai/wahajahmed010/overleaf-latex) <br>
- [LaTeX Resume Patterns](references/latex-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and LaTeX examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local git, pdflatex, Overleaf credentials, and the optional Overleaf plugin workflow.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
