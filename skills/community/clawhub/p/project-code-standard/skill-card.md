## Description: <br>
Project Code Standard helps developers check, enforce, and optionally fix project code standards across Python, JavaScript/TypeScript, and general repository structure conventions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[forestxieCode](https://clawhub.ai/user/forestxieCode) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to identify project type, run suitable linting or formatting checks, summarize issues in a Markdown report, and prepare starter code-quality configuration when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional automated fixes can modify repository files or apply formatting changes the user did not intend. <br>
Mitigation: Require explicit user confirmation before running fix commands, keep changes under version control, and review diffs after changes. <br>
Risk: The artifact references helper scripts and starter templates that were not included in the reviewed package. <br>
Mitigation: Verify referenced scripts and templates exist and are trusted before executing them or copying them into a project. <br>
Risk: Lint or formatting recommendations may conflict with a project's established standards. <br>
Mitigation: Prefer existing project lint configuration and review the generated Markdown report before adopting changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/forestxieCode/project-code-standard) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/forestxieCode) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional fixes require user confirmation before files are modified.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
