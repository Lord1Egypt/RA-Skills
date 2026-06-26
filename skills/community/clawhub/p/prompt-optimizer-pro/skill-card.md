## Description: <br>
Prompt Optimizer helps users improve, diagnose, score, translate, compare, and save prompts for common LLM workflows while keeping its prompt library and history local. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mkpareek0315](https://clawhub.ai/user/mkpareek0315) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and employees use this skill to turn vague prompts into structured, model-agnostic instructions, build prompt templates, and manage a local prompt library. It is suited for prompt-writing assistance across writing, coding, analysis, support, and creative tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved prompts and history may contain API keys, passwords, private customer data, or proprietary prompts because the skill keeps a local prompt library and history. <br>
Mitigation: Do not save sensitive prompts unless local retention is acceptable; delete ~/.openclaw/prompt-optimizer/ to remove the saved library and history. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mkpareek0315/prompt-optimizer-pro) <br>
- [Publisher profile](https://clawhub.ai/user/mkpareek0315) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with prompt templates, before-and-after rewrites, scoring tables, and occasional JSON or shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores settings, saved prompts, and prompt history under ~/.openclaw/prompt-optimizer/ when the agent follows the artifact workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
