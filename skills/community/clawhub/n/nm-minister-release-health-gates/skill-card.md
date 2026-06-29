## Description: <br>
Standardizes release approvals with GitHub-aware checklists and deployment gates before production releases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Release managers, developers, QA, and SRE teams use this skill before production releases to assemble GitHub-aware release gate checklists, summarize quality signals, document waivers, and capture rollout scorecards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated PR comments, tracker updates, or sign-off summaries could be treated as final release approval without enough review. <br>
Mitigation: Have release owners review the generated gate snippet, tracker updates, waiver records, and sign-off evidence before deployment. <br>
Risk: Broad release, GitHub, readiness, quality, and governance triggers can load the skill during general release conversations. <br>
Mitigation: Confirm the skill is being used for release-readiness checklist work before applying its guidance. <br>


## Reference(s): <br>
- [Project homepage from ClawHub metadata](https://github.com/athola/claude-night-market/tree/master/plugins/minister) <br>
- [Deployment Readiness Gate](modules/deployment-readiness.md) <br>
- [Quality Signals Gate](modules/quality-signals.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance, configuration] <br>
**Output Format:** [Markdown checklists, PR or issue comment snippets, summaries, and scorecards] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces release gate snippets, QA handshake summaries, and rollout scorecards for human review.] <br>

## Skill Version(s): <br>
1.9.13 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
