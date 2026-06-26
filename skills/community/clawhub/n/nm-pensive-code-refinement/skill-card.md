## Description: <br>
Improves code quality across duplication, efficiency, and architectural fit. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to analyze living code for duplication, algorithmic inefficiency, clean-code issues, architectural fit, anti-slop patterns, error handling gaps, and additive bias. It produces prioritized refactoring plans and can optionally execute scoped changes when explicitly requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Aggressive invocation phrases can expand the workflow beyond ordinary planning and scope limits. <br>
Mitigation: Keep requests narrow and avoid phrases such as "ignore scope guard," "execute all findings," or "do not stop" unless broad execution is intended. <br>
Risk: The insight-generation module can publish refinement findings to GitHub Discussions. <br>
Mitigation: Do not load or run insight generation unless external publication is intended, and review and redact findings before posting. <br>
Risk: Automated refactoring proposals or edits may introduce incorrect guidance or code changes. <br>
Mitigation: Review the generated plan, evidence, and any code changes before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-pensive-code-refinement) <br>
- [Project homepage from Clawdis metadata](https://github.com/athola/claude-night-market/tree/master/plugins/pensive) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, structured findings, refactoring plans, and optional code changes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tiered analysis levels are supported; execution scope depends on the user's invocation.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
