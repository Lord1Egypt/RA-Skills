## Description: <br>
Transforms messages that begin with `@prt` or `@prompt` into structured, copy-ready prompts, with concise clarification and natural bypass behavior for incomplete or non-target inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keyzzzoe](https://clawhub.ai/user/keyzzzoe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, builders, and general AI users use this skill to turn natural-language requests into compact prompts for coding, prototyping, planning, research-style information gathering, and other build-oriented tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated prompts may carry sensitive information or high-impact instructions into another model. <br>
Mitigation: Review generated prompts before reuse, especially when the original request involves sensitive data or consequential actions. <br>
Risk: Prompt transformations can make unsuitable assumptions when a request is underspecified. <br>
Mitigation: Use the skill's clarification path for major gaps and review any stated assumptions before copying the prompt. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/keyzzzoe/prompt-transformer) <br>
- [Decision Guide](references/decision-guide.md) <br>
- [Prompt Patterns](references/prompt-patterns.md) <br>
- [Examples](references/examples.md) <br>
- [English Guide](references/guide-en.md) <br>
- [Chinese Guide](references/guide-zh.md) <br>
- [Debug and Iteration History](references/debug-history.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown prompt text with a short handling summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask one to three clarification questions or answer naturally when a prefixed message is ordinary chat.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
