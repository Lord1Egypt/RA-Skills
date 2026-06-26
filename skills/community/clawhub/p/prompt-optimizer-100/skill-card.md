## Description: <br>
Optimizes user requests by classifying task complexity, restructuring prompts across role, context, task, constraints, and examples, and routing work to single or parallel agents when appropriate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liyu9](https://clawhub.ai/user/liyu9) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to turn informal requests into structured prompts, classify work from L1 to L4, and apply confirmation or multi-agent routing for higher-risk tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently changes agent memory, so future requests may be automatically rewritten or executed without clear per-use consent. <br>
Mitigation: Install only when global prompt optimization is intended, back up and review agent-notes.md, and prefer merge mode over overwrite. <br>
Risk: Sensitive, external, or side-effecting tasks may be optimized and executed before the user reviews the rewritten prompt. <br>
Mitigation: Use explicit wording such as asking the agent to show the optimized prompt first before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liyu9/prompt-optimizer-100) <br>
- [Publisher profile](https://clawhub.ai/user/liyu9) <br>
- [Prompt optimization rules](artifact/rules/prompt-optimization.md) <br>
- [Installation and usage guide](artifact/SKILL.md) <br>
- [System design document](https://feishu.cn/docx/He9Gdnpd4oTydyxSAZYcVQ1dnTc) <br>
- [PromptPilot reference](https://www.producthunt.com/products/promptpilot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands, configuration] <br>
**Output Format:** [Markdown text with prompt plans, task classifications, comparison tables, and installation or verification commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist prompt-optimization rules into OpenClaw agent memory during installation.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
