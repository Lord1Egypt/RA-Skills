## Description: <br>
Systematic debugging framework. 4-phase root-cause analysis with defense-in-depth. Never guess, never patch symptoms. From Claude Code + Superpowers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxiaofei860208-source](https://clawhub.ai/user/wangxiaofei860208-source) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to guide agents through root-cause debugging, replacing guesswork and symptom patches with reproduction, investigation, condition-based waiting, layered prevention, and verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may lead an agent to inspect code, run tests, add diagnostics, and propose code changes during debugging. <br>
Mitigation: Use it in development workspaces where those actions are approved, and review proposed changes before applying them. <br>
Risk: The strict no-fixes-before-root-cause workflow can delay quick symptom relief when an urgent workaround is needed. <br>
Mitigation: Treat emergency workarounds as temporary, document them, and return to the root-cause investigation and verification process. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangxiaofei860208-source/lobster-debugging) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Analysis, Code, Shell commands] <br>
**Output Format:** [Markdown guidance with optional code and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide an agent to inspect code, run tests, add diagnostics, and propose changes during debugging.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
