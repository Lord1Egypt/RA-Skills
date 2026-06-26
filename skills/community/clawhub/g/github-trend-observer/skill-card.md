## Description: <br>
A GitHub intelligence tool for AI product managers that uses the local authenticated GitHub CLI and GitHub API to discover projects, monitor trend signals, and generate PM-grade paradigm insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Kun-0546](https://clawhub.ai/user/Kun-0546) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product managers, and AI ecosystem analysts use this skill to discover GitHub projects, search technical directions, monitor growth anomalies, and analyze a repository's ecosystem and competitive context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses the user's local authenticated GitHub CLI session and consumes GitHub API quota. <br>
Mitigation: Confirm the intended account with gh auth status and run the skill only for repository research that should use that account's access and quota. <br>
Risk: Generated HTML reports may include repository data from unfamiliar projects and report fields are not consistently escaped. <br>
Mitigation: Treat generated HTML as untrusted local output, review the source context, and avoid opening or sharing reports from searches that include untrusted repository metadata. <br>
Risk: Anomaly monitoring currently focuses on new projects and does not fully detect sudden surges in established projects without persistent comparison data. <br>
Mitigation: Use the signal watch output as a discovery aid, not a complete monitoring system, and add persistent history before relying on it for established-project alerting. <br>


## Reference(s): <br>
- [Layer Model](artifact/references/layer_model.md) <br>
- [GitHub CLI](https://cli.github.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/Kun-0546/github-trend-observer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports and local HTML reports with inline tables, analysis sections, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the authenticated local GitHub CLI session and GitHub API quota; report depth may degrade when quota is low.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
