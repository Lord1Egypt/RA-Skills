## Description: <br>
Runs multi-source research across GitHub, HN, Reddit, arXiv, and Semantic Scholar. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and research-oriented agent users use this skill to coordinate a multi-source technical research session, synthesize findings, and produce a saved report or brief. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger words may invoke the research workflow unexpectedly. <br>
Mitigation: Confirm the user intended to start a multi-source research session before dispatching agents. <br>
Risk: Research results may include external-source content and saved reports that are inappropriate for sensitive workspaces. <br>
Mitigation: Review generated docs/research outputs before sharing or committing them. <br>


## Reference(s): <br>
- [Tome plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/tome) <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-tome-research) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries and reports, with structured JSON findings used during synthesis.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save research reports under docs/research/ and preserve session state for follow-up refinement.] <br>

## Skill Version(s): <br>
1.9.12 (source: server evidence release; artifact frontmatter says 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
