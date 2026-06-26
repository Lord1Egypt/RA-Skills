## Description: <br>
AI-powered academic paper reviewer. Uses a multi-agent system (Deconstructor, Devil's Advocate, Judge) to analyze papers for logical flaws, contradictions, and empirical validity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sschepis](https://clawhub.ai/user/sschepis) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Researchers, reviewers, and developers use this skill to review academic papers or scientific claims for logical flaws, contradictions with literature, empirical validity, and concrete improvement suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Manuscript or claim content may be sent to configured external LLM and search providers. <br>
Mitigation: Avoid confidential or unpublished material unless the configured providers' data handling terms are acceptable. <br>
Risk: Search execution may use shell-based handling of document-derived text. <br>
Mitigation: Avoid SkillSearchAdapter or serper-tool use until shell execution is replaced with safe argument-based execution. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [analysis, json, guidance] <br>
**Output Format:** [JSON merit report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes an overall score, defense strategy, improvement suggestions, and dimension scores for logic, novelty, and related review criteria.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
