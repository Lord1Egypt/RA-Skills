## Description: <br>
Open prompt stack for public-market investment research that routes agents through structured company, industry, earnings, consensus, catalyst, red-team, briefing, and portfolio-manager workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joansongjr](https://clawhub.ai/user/joansongjr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investment analysts, portfolio managers, and research teams use this skill to make AI-assisted public-market research more structured, evidence-graded, and easier to archive across companies, industries, earnings events, catalysts, and red-team reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to trigger broadly and coordinate multiple research modes, which can lead to unintended agent actions if installed globally. <br>
Mitigation: Install it in a dedicated investment-research workspace and review the trigger and routing rules before enabling broad use. <br>
Risk: The skill can read, persist, or update local research files such as bias logs, decision logs, checkpoints, coverage files, and archived outputs. <br>
Mitigation: Set explicit archive and checkpoint locations, limit the workspace to intended research files, and define cleanup rules before using persistent workflows. <br>
Risk: Financial research outputs may include incomplete, stale, or unverified market assumptions. <br>
Mitigation: Require human review of evidence grades, unknowns, and compliance statements before relying on outputs for investment decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/joansongjr/investor-harness) <br>
- [Publisher profile](https://clawhub.ai/user/joansongjr) <br>
- [README](README.md) <br>
- [Evidence grading system](core/evidence.md) <br>
- [Compliance boundaries](core/compliance.md) <br>
- [Data source adapters](core/adapters.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown research briefs, checklists, structured prompts, and file-oriented workflow guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include evidence grades, assumptions, follow-up data gaps, suggested archive paths, and compliance reminders.] <br>

## Skill Version(s): <br>
0.6.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
