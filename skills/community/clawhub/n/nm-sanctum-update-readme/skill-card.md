## Description: <br>
Refreshes README structure and content using repo context and exemplar research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to refresh README structure after meaningful project changes. It audits repository languages, researches comparable README examples, aligns the outline, applies documentation edits, scans for formulaic AI prose, and reports verification details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documentation or agent guidance edits could affect future repository workflows and tooling behavior. <br>
Mitigation: Use report-only mode for sensitive repositories and review proposed changes to README, AGENTS, CONTRIBUTING, .agents, and .cursor files before applying them. <br>
Risk: External README exemplar research may introduce outdated or poorly matched documentation patterns. <br>
Mitigation: Retain citations for selected exemplars, check recency and maintainer activity, and adapt only patterns that match the current repository evidence. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-sanctum-update-readme) <br>
- [Publisher profile](https://clawhub.ai/user/athola) <br>
- [OpenClaw homepage](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum) <br>
- [Language audit patterns](modules/language-audit.md) <br>
- [Exemplar research patterns](modules/exemplar-research.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown reports, README edits, command snippets, and verification summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May edit README.md or another specified documentation file; report-only review is recommended for sensitive repositories.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
