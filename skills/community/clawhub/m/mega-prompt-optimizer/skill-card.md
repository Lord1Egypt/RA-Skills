## Description: <br>
Mega Prompt Optimizer turns vague user requests into structured prompts by matching user intent against a curated prompt-template library and presenting an optimized prompt for confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thomaszhou22](https://clawhub.ai/user/thomaszhou22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn informal requests into clearer prompts for writing, coding, analysis, translation, business, and other tasks. The skill is designed to stay off until explicitly enabled and to show the optimized prompt for user review before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled prompt library includes unsafe templates that could be recommended during normal use. <br>
Mitigation: Review every optimized prompt before using it, keep the optimizer off by default, and remove or filter unsafe templates before shared or production use. <br>
Risk: The optimizer could be used for jailbreaks, memory or system-prompt disclosure, unauthorized security testing, credential handling, or regulated medical, legal, or financial advice. <br>
Mitigation: Avoid using it for those cases, decline or remove templates that support them, and require qualified review before any regulated advice use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thomaszhou22/mega-prompt-optimizer) <br>
- [Prompt library lite](artifact/references/prompt_library_lite.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown preview with the original request, optimized prompt, change summary, and referenced template.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit opt-in and user confirmation before the optimized prompt is used.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
