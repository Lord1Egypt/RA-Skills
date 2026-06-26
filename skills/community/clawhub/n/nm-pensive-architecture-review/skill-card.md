## Description: <br>
Assesses architecture decisions, ADR compliance, and coupling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering reviewers use this skill to assess architecture changes before merging, including ADR compliance, coupling, invariant conflicts, principle checks, and follow-up actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad architecture and design trigger wording may activate the skill during general design discussions. <br>
Mitigation: Review the triggers before installing and invoke the skill for explicit architecture, ADR, coupling, or structural design reviews. <br>
Risk: Architecture recommendations can be treated as final decisions without enough human review. <br>
Mitigation: Require evidence-backed findings and keep invariant conflicts escalated to a human decision maker before accepting preserve, layer, or revise options. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-pensive-architecture-review) <br>
- [OpenClaw homepage](https://github.com/athola/claude-night-market/tree/master/plugins/pensive) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Analysis, Shell commands, Guidance] <br>
**Output Format:** [Markdown with checklists, review findings, diagrams, recommendations, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ADR audit results, before/after interaction maps, invariant conflict options, principle-check findings, and approve/block recommendations.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
