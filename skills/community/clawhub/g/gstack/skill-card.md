## Description: <br>
Fast headless browser for QA testing and site dogfooding, plus workflow skills for planning, review, shipping, QA, retrospectives, and release documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OVYEDDeno](https://clawhub.ai/user/OVYEDDeno) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use Gstack to give coding agents specialized workflows for product planning, technical design review, code review, release execution, browser-based QA, and release documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Imported browser cookies can grant access to real authenticated accounts. <br>
Mitigation: Treat imported cookies as account credentials and import only the specific domains intentionally needed for testing. <br>
Risk: Workflow skills can mutate repositories through code edits, documentation updates, commits, and release actions. <br>
Mitigation: Review proposed repository changes, especially /ship and /document-release output, before using the skill on sensitive repositories. <br>
Risk: Auto-upgrade behavior can change future skill behavior without manual review. <br>
Mitigation: Enable auto-upgrade only when the publisher and future upstream changes are trusted. <br>
Risk: Persisted workflow and browser state may contain sensitive project or session context. <br>
Mitigation: Use the skill only in trusted workspaces and clear persisted state when handling sensitive projects. <br>


## Reference(s): <br>
- [ClawHub Gstack Skill Page](https://clawhub.ai/OVYEDDeno/gstack) <br>
- [README](README.md) <br>
- [Architecture](ARCHITECTURE.md) <br>
- [Browser Automation Guide](BROWSER.md) <br>
- [QA Issue Taxonomy](qa/references/issue-taxonomy.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, structured reports, code edits, screenshots, and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write workflow state, QA artifacts, documentation updates, repository changes, browser screenshots, and release notes depending on the invoked sub-skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
