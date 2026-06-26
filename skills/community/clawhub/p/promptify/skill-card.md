## Description: <br>
Optimize prompts for clarity and effectiveness, with optional routing for clarifying questions, codebase context, or web research when the prompt calls for it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tolibear](https://clawhub.ai/user/tolibear) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, writers, analysts, and other agent users use this skill to turn vague or underspecified prompts into clearer prompts with explicit role, task, constraints, and output expectations. It can ask clarifying questions, gather project context, or research current practices when those modes are requested or detected. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Codebase-aware prompt optimization may inspect relevant project files when +deep is used or when codebase context is auto-detected. <br>
Mitigation: Review prompts for secrets or private project details before using codebase-context modes, and limit the prompt scope to information needed for the optimization task. <br>
Risk: Web research modes may send prompt-derived search terms to external search tools. <br>
Mitigation: Avoid using +web or current-practice prompts with sensitive, proprietary, or confidential details unless those terms are safe to disclose. <br>
Risk: The skill may produce clipboard shell commands for the optimized prompt. <br>
Mitigation: Review generated clipboard commands before running them, especially when prompts contain quoting, shell metacharacters, or sensitive text. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tolibear/promptify) <br>
- [README](artifact/README.md) <br>
- [Promptify command](artifact/commands/promptify.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with an optimized prompt code block, optional clipboard command, and a short explanation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include clarifying questions, concise research summaries, or codebase context summaries when those modes are triggered.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
