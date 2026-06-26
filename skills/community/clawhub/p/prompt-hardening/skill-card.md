## Description: <br>
Systematic methods for hardening LLM agent prompts to reliably follow instructions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and prompt authors use this skill to audit and strengthen agent, system, and operational prompts when agents ignore rules, bypass constraints, or drift during long conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt hardening advice can be misapplied as a substitute for code-level enforcement or accepted without reviewing the suggested changes. <br>
Mitigation: Treat outputs as advisory, inspect suggested prompt changes before applying them, and use code-level controls for critical constraints. <br>


## Reference(s): <br>
- [Detailed Pattern Descriptions](references/patterns.md) <br>
- [Prompt Hardening Research Sources](references/sources.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/lanyasheng/prompt-hardening) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with optional shell command examples and audit checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces advisory prompt audits, hardened prompt drafts, and violation analyses; it does not modify target prompts automatically.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
