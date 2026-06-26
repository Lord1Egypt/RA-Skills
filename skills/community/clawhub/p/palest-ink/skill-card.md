## Description: <br>
Palest Ink tracks local development activity, browsing history, shell commands, editor activity, app focus, and file changes so an agent can answer activity-recall and daily-report questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billhandsome52](https://clawhub.ai/user/billhandsome52) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to query local activity records, generate daily or weekly work summaries, and search past Git, browser, shell, editor, app-focus, and file-change activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs broad continuous local monitoring of browsing, shell commands, editor activity, app and window titles, file changes, and Git activity. <br>
Mitigation: Install only when this monitoring is explicitly desired; review the configuration, disable unnecessary collectors, and narrow watched directories and exclusions before use. <br>
Risk: Global Git hooks and a LaunchAgent can continue running in the background after installation. <br>
Mitigation: Review the installed hooks and LaunchAgent, and use the provided uninstall flow when background collection is no longer needed. <br>


## Reference(s): <br>
- [Palest Ink ClawHub release](https://clawhub.ai/billhandsome52/palest-ink) <br>
- [Palest Ink Data Schema](references/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured activity summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local JSONL activity records stored under ~/.palest-ink when installed.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
