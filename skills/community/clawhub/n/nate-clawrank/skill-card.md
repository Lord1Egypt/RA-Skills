## Description: <br>
Clawrank is an agent performance scoring system for OpenClaw agents that scores seven evidence-based dimensions on a normalized 100-point scale, assigns performance tiers, supports trajectory tracking, and can integrate peer review via agent-sync. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joeycacciatore3](https://clawhub.ai/user/joeycacciatore3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use Clawrank at session end or on explicit self-evaluation requests to produce evidence-backed performance scores, tiers, and weekly trends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad self-evaluation phrases may trigger scoring when the user did not intend to request a formal Clawrank report. <br>
Mitigation: Invoke Clawrank explicitly for formal scoring and treat mid-session checks as estimates. <br>
Risk: Score evidence, peer review, or weekly tracking may expose sensitive user or project details. <br>
Mitigation: Keep scoring evidence concise and omit sensitive details when sharing, reviewing, or tracking scores. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown score report with tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes seven dimension scores, evidence lines, raw and final totals, a tier, optional weekly trend tracking, and optional peer-review averaging.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
