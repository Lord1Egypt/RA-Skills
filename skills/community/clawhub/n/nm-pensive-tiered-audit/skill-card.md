## Description: <br>
Runs a gated, three-tier codebase audit that starts with git-history review, escalates to targeted source review when evidence warrants it, and requires approval for full-codebase audit. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering reviewers use this skill to audit codebase changes before release, before merge, or after instability by collecting evidence from git history and escalating to deeper review only when criteria are met. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad audit and review triggers may activate the skill during ordinary review discussions. <br>
Mitigation: Confirm the audit scope and commit range before running the workflow. <br>
Risk: Deeper tiers can read repository source files and write local .coordination findings. <br>
Mitigation: Run the skill only in the intended repository and review generated findings before sharing them. <br>
Risk: A full-codebase audit can consume substantial context and compute. <br>
Mitigation: Use the Tier 3 gate and proceed only after explicit user approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-pensive-tiered-audit) <br>
- [Skill homepage](https://github.com/athola/claude-night-market/tree/master/plugins/pensive) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown findings files with evidence-tagged sections and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local .coordination/agents/*.findings.md files during audit workflows; Tier 3 requires explicit user approval.] <br>

## Skill Version(s): <br>
1.9.12 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
