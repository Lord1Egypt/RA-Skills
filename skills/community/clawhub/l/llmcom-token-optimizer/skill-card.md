## Description: <br>
Token-efficient context format using LLMCOM specification - reduces token usage by 70-80% through compact object notation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shalinda-j](https://clawhub.ai/user/shalinda-j) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to compact structured context into LLMCOM notation, parse LLMCOM back into JSON-compatible data, and estimate token savings for agent requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The advertised 70-80% token savings are estimates and may not match a target model's tokenizer. <br>
Mitigation: Validate savings with the tokenizer and prompts used in the target deployment before relying on the estimate. <br>
Risk: The documentation mentions slash commands and integrations that are not provided by the included code. <br>
Mitigation: Use the included Python API or add the missing command wrappers before depending on slash-command workflows. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shalinda-j/llmcom-token-optimizer) <br>
- [GitHub link listed in skill documentation](https://github.com/shalinda-j/LLMCOM) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, guidance] <br>
**Output Format:** [LLMCOM text, JSON-compatible dictionaries, Markdown guidance, and local Python command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses approximate token counting; the advertised savings should be validated against the target tokenizer.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
