## Description: <br>
Web SaaS service decomposition and AI internalization development plan generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mupengi-bot](https://clawhub.ai/user/mupengi-bot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and business planners use this skill to decompose public SaaS services into functions, score AI replaceability, compare competing products, and draft internalization roadmaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Analyzing private or logged-in SaaS pages could expose sensitive information or rely on access the skill is not meant to use. <br>
Mitigation: Use explicit public SaaS targets and avoid private or logged-in pages. <br>
Risk: Referenced memory files or generated event JSON may introduce stale or unsupported assumptions into downstream planning. <br>
Mitigation: Review local memory files and generated saas-analysis event files before downstream skills rely on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mupengi-bot/mupeng-saas-decomposer) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, configuration, guidance] <br>
**Output Format:** [Markdown reports with decomposition tables, roadmap sections, skill draft guidance, and optional JSON event files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce saas-analysis event JSON for downstream planning skills.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
