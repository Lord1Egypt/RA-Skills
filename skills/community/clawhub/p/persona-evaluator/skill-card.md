## Description: <br>
Audits OpenPersona persona packs and peer LLM agents through structural CLI checks, semantic white-box review, and consent-aware black-box review, producing scored quality reports with strengths, issues, and actionable improvements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neiljo-gy](https://clawhub.ai/user/neiljo-gy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to evaluate OpenPersona personas for structural completeness, narrative quality, role fit, boundary clarity, and identity coherence. It supports CI-style checks, self-review, peer review, and black-box review when source files are not available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may ask an agent to run OpenPersona CLI commands against local persona packs. <br>
Mitigation: Review the target persona and command before execution, especially when commands read pack content or write reports. <br>
Risk: Remediation steps such as refine --apply, update, or direct persona.json edits can change persona behavior. <br>
Mitigation: Treat proposed fixes as reviewable changes and approve them before applying or committing modifications. <br>
Risk: Black-box review can involve interacting with remote agents or reviewing public material with lower confidence. <br>
Mitigation: Respect the skill's consent tiers, label passive observation clearly, and avoid treating black-box scores as equivalent to white-box source review. <br>


## Reference(s): <br>
- [persona-evaluator on ClawHub](https://clawhub.ai/neiljo-gy/persona-evaluator) <br>
- [OpenPersona repository](https://github.com/acnlabs/OpenPersona) <br>
- [persona-evaluator standalone repository](https://github.com/acnlabs/persona-evaluator) <br>
- [OpenPersona skill listing](https://openpersona.co/skill/persona-evaluator) <br>
- [Semantic Evaluation Report Formats](references/REPORT-FORMAT.md) <br>
- [Black-box Semantic Evaluation](references/BLACK-BOX.md) <br>
- [White-box Semantic Rubrics](references/RUBRICS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with inline shell commands and optional JSON-producing CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include dimension scores, confidence labels for black-box reviews, strengths, issues, and concrete remediation guidance.] <br>

## Skill Version(s): <br>
0.3.4 (source: release evidence, frontmatter metadata, and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
