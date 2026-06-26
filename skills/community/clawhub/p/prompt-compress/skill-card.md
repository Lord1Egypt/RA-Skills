## Description: <br>
Prompt Compress helps agents analyze and shorten prompts by extracting keywords, removing redundant wording, and preserving the prompt's intended meaning to reduce token use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackzh1982](https://clawhub.ai/user/jackzh1982) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, prompt engineers, and other agent users use this skill to compress long prompts, extract core requirements, and reduce token cost while retaining the original task intent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Compressed prompts can drop nuance, constraints, or context in sensitive or complex instructions. <br>
Mitigation: Review compressed prompts before sending them onward, especially for legal, medical, security, or other high-impact tasks. <br>
Risk: Token counts are estimates and may differ from model-specific tokenizer results. <br>
Mitigation: Verify final token counts with the tokenizer for the target model when exact limits or costs matter. <br>


## Reference(s): <br>
- [Token Calculation Reference](references/token-calculation.md) <br>
- [ClawHub release page](https://clawhub.ai/jackzh1982/prompt-compress) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown with token estimates, savings percentage, and compressed prompt text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses approximate token estimates and supports multiple compression levels from light to minimal.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
