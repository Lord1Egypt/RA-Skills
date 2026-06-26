## Description: <br>
Nm Minister Release Health Gates helps agents standardize production release approvals with GitHub-aware readiness, quality, documentation, operations, and waiver gates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Use before production releases to generate release gate checklists, QA handoff summaries, and rollout scorecards that make blockers, approvals, rollback ownership, documentation, and observability readiness explicit. <br>

### Deployment Geography for Use: <br>
Not geography-specific; suitable wherever ClawHub skills and GitHub-based release workflows are permitted. <br>

## Known Risks and Mitigations: <br>
Risk: Broad triggers such as release and GitHub could activate the skill in adjacent workflows where a formal production gate is not needed. <br>
Mitigation: Confirm the release context before using its output, and keep final approval for publishing, deployment, or repository-changing actions under user control. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-minister-release-health-gates) <br>
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/minister) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance, configuration] <br>
**Output Format:** [Markdown release gate snippets, QA handshake summaries, checklist sections, and rollout scorecards.] <br>
**Output Parameters:** [Release name, deployment PR or issue links, GitHub check status, blocker list, documentation status, observability links, support notes, rollback owner, and approval or waiver state.] <br>
**Other Properties Related to Output:** [Outputs are intended for review in pull requests, issues, trackers, and release retrospectives before deployment decisions are finalized.] <br>

## Skill Version(s): <br>
1.9.12 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
