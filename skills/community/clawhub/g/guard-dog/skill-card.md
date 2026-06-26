## Description: <br>
Guard-Dog intercepts eight classes of risky AI operations and requires authorization-code verification before allowing them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[staroldtrace](https://clawhub.ai/user/staroldtrace) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to add an authorization gate around risky AI actions such as financial operations, sensitive-data access, destructive commands, prompt-injection attempts, source access, history replay, and changes to the guard skill itself. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner did not fully verify artifact file contents. <br>
Mitigation: Review the bundled skill files before installation or redistribution when high assurance is required. <br>
Risk: Authorization input may be captured by the surrounding runtime, conversation history, or platform logs. <br>
Mitigation: Use the skill only in a trusted runtime with sensitive-input logging disabled or controlled. <br>
Risk: The skill stores authorization state on the local filesystem. <br>
Mitigation: Keep ~/.openclaw/.guard-dog-vault and ~/.openclaw/.guard-dog-state restricted to owner read/write permissions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/staroldtrace/guard-dog) <br>
- [Common attack pattern guide](references/attack-patterns.md) <br>
- [Guard-dog iron rules](references/iron-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with authorization prompts, pass/fail status messages, configuration notes, and occasional shell command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes and reads local guard state under ~/.openclaw with 600 permissions; responses should never disclose, repeat, or hint at authorization codes.] <br>

## Skill Version(s): <br>
2.1.3 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
