## Description: <br>
PromptBuddy rewrites user requests into structured optimized prompts, shows a short preview of the optimized prompt, and then helps answer or skips optimization for simple queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steventsang18](https://clawhub.ai/user/steventsang18) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to see how an informal request is transformed into a structured prompt before receiving an answer. The skill is also intended to bypass optimization for simple queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to inspect and rewrite every user message, which may expose sensitive prompt content. <br>
Mitigation: Use only with explicit opt-in for conversations where prompt content can be shared with the optimizer, and avoid sending sensitive or regulated information. <br>
Risk: The submitted artifact references a local optimizer script that is not included for review. <br>
Mitigation: Require the publisher to include and document the optimizer script before trusting execution, and review the script before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/steventsang18/prompt-buddy) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown text with JSON-derived prompt excerpts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Shows the first 6-8 lines of optimized_prompt when available; skips optimization for simple queries.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
