## Description: <br>
幻觉检测器 helps agents review AI-generated code for hallucinated APIs, incorrect parameters, false references, version mismatches, type errors, and contradictory logic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, code reviewers, and AI coding assistants use this skill to inspect AI-generated code for hallucinated APIs, wrong parameters, fake documentation links, invalid package references, type mistakes, and impossible logic. It produces a structured review report with severity, confidence, and suggested fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Findings can be incomplete or incorrect when dependency versions, runtime context, or project-specific APIs are missing. <br>
Mitigation: Provide relevant package versions and project context, then verify findings against tests, official documentation, or a human code review. <br>
Risk: The skill's report may be mistaken for a substitute for full quality assurance. <br>
Mitigation: Use it as an initial review aid and continue to run normal tests, documentation checks, and human review before accepting changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/534422530/hallucination-detector) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown hallucination detection report with findings, severity, confidence, and suggested fixes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings may reference code locations and classify API, version, reference, type, and logic hallucinations.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
