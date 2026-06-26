## Description: <br>
Scores backlog items with RICE, WSJF, and Kano methods and files GitHub issues for top candidates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product managers, and roadmap owners use this skill to inventory features, classify them, score backlog priorities, analyze tradeoffs, and turn accepted high-priority suggestions into GitHub issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence flags automatic local persistence and broad repository handling. <br>
Mitigation: Confirm the paths the skill inspects before use and disable or manually approve deferred capture when automatic local writes are not acceptable. <br>
Risk: Optional research enrichment can broaden handling to external research channels. <br>
Mitigation: Enable research mode only when external evidence collection is appropriate for the repository and review the resulting evidence before changing priorities. <br>
Risk: The skill can generate GitHub issues from prioritized suggestions. <br>
Mitigation: Review issue titles, bodies, labels, and linked context before allowing issue creation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-imbue-feature-review) <br>
- [Publisher profile](https://clawhub.ai/user/athola) <br>
- [Clawdis homepage](https://github.com/athola/claude-night-market/tree/master/plugins/imbue) <br>
- [Scoring framework](artifact/modules/scoring-framework.md) <br>
- [Classification system](artifact/modules/classification-system.md) <br>
- [Tradeoff dimensions](artifact/modules/tradeoff-dimensions.md) <br>
- [Research enrichment](artifact/modules/research-enrichment.md) <br>
- [Configuration](artifact/modules/configuration.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown tables, prioritization reports, issue drafts, configuration examples, and shell command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include research evidence when enabled and GitHub issue content for accepted suggestions.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata; artifact frontmatter lists 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
