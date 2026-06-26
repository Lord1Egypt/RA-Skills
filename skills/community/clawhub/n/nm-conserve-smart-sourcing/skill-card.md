## Description: <br>
Selects optimal sources for tool calls, balancing accuracy with token cost. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to decide when factual claims need citations, when an uncertainty note is enough, and when source-gathering cost outweighs verification value. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad sourcing triggers can cause an agent to search or cite sources when that behavior is not desired. <br>
Mitigation: Review the triggers and citation decision rules before installation, especially for agents where extra searches or citations would be disruptive. <br>
Risk: The linked Claude Code plugin may include behavior outside this Markdown guidance skill. <br>
Mitigation: Evaluate the linked plugin separately before installing any agents, hooks, or commands from it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-conserve-smart-sourcing) <br>
- [Conserve plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/conserve) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown] <br>
**Output Format:** [Markdown guidance with citation decision rules and examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable output; influences when an agent searches for and cites sources.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata; artifact frontmatter lists 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
