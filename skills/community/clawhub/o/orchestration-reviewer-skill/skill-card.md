## Description: <br>
Reviews existing workflow Plan IRs for goal alignment, topology, skill binding, scope safety, executability, efficiency, and governance, then returns a decision, issues, scores, and suggested revisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tuobadaidai](https://clawhub.ai/user/tuobadaidai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workflow operators use this skill to review an existing workflow plan before execution. It checks whether the plan matches the business goal, is structurally executable, uses appropriate skills, limits state scope, and provides actionable governance findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review findings or revision suggestions could be mistaken for approval to execute a workflow. <br>
Mitigation: Treat outputs as governance guidance only, and manually inspect any suggested revisions before using them in a real workflow. <br>
Risk: Incomplete or inaccurate Plan IR and skill manifest inputs can lead to incorrect review conclusions. <br>
Mitigation: Provide only the plan and skill manifest data needed for review, then re-run schema, topology, and scope validation before adopting revisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tuobadaidai/orchestration-reviewer-skill) <br>
- [Review Manual](artifact/references/review-manual.md) <br>
- [Review Rules](artifact/references/review-rules.md) <br>
- [Scoring Policy](artifact/references/scoring-policy.md) <br>
- [Security Guardrails](artifact/references/security-guardrails.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Structured JSON review results with concise guidance, scorecards, issue lists, and optional revised Plan IR and diff report.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a business goal, an existing Plan IR, and available skill metadata; review-only use does not execute the plan.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
