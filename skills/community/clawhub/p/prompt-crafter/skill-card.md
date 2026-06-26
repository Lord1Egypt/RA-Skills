## Description: <br>
Build AI prompts that actually work for ChatGPT, Claude, Gemini, or any LLM, covering RACE, Chain-of-Thought, Constraint-Stacking, Few-Shot examples, troubleshooting, and production safety rules while excluding image-generation prompting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Crispyangles](https://clawhub.ai/user/Crispyangles) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, operators, and other LLM users use this skill to choose prompt frameworks, draft stronger text prompts, troubleshoot weak model outputs, and apply basic prompt safety practices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt examples include adversarial phrases that could be mistaken for operational instructions. <br>
Mitigation: Treat adversarial phrases in examples as hardening test inputs and preserve existing system and safety rules. <br>
Risk: Prompt-writing guidance may produce incorrect or misleading downstream model outputs if used without review. <br>
Mitigation: Review generated prompts and resulting model outputs before deployment or publication. <br>


## Reference(s): <br>
- [Prompt Frameworks - Extended Examples](references/frameworks.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, text, configuration] <br>
**Output Format:** [Markdown guidance with prompt templates and examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no executable behavior or privileged access.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
