## Description: <br>
观势 is an AI strategy-analysis skill that uses enterprise lifecycle positioning, BLM, a six-step insight method, and strategy frameworks to produce structured strategic diagnosis, market and competition analysis, implementation recommendations, and optional PPT outlines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tuobadaidai](https://clawhub.ai/user/tuobadaidai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business users, strategy teams, and analysts use this skill to turn strategic questions into structured reports covering lifecycle stage, market entry or exit, competition, organization fit, business model, growth options, and execution plans. It is not intended for simple fact lookup, policy Q&A, or casual conversation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist sensitive company strategy analysis, including generated PPT outline content. <br>
Mitigation: Avoid sharing confidential business data unless the workspace is approved for it, and review or remove generated output files before wider distribution. <br>
Risk: The initializer can install or create local expert skill dependencies, and evidence.security warns against running it with --yes without intent. <br>
Mitigation: Run initialization interactively, review each dependency and its publisher before installation, and avoid --yes unless local skill creation is expected. <br>
Risk: Strategic recommendations may be incorrect, incomplete, or misleading if source data is weak or unverifiable. <br>
Mitigation: Require human review of assumptions, citations, financial data, and proposed decisions before operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tuobadaidai/skills/guanshi) <br>
- [lifecycle-model.md](references/lifecycle-model.md) <br>
- [six-steps.md](references/six-steps.md) <br>
- [strategy-frameworks.md](references/strategy-frameworks.md) <br>
- [output-spec.md](references/output-spec.md) <br>
- [audit-checklist.md](references/audit-checklist.md) <br>
- [scheduling-protocol.md](references/scheduling-protocol.md) <br>
- [expert-registry.md](references/expert-registry.md) <br>
- [ppt-bridge-protocol.md](references/ppt-bridge-protocol.md) <br>
- [install-publish-guide.md](references/install-publish-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with optional JSON PPT outline and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a PPT outline to output/guanshi-ppt-outline.json for medium or complex analyses.] <br>

## Skill Version(s): <br>
3.2.1 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
