## Description: <br>
Hermes Self-Evolution Skills supports memory management and skill tracking for OpenClaw agents by prompting for memory saves, compressing context, saving discovered techniques as skills, and applying security checks before memory writes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add periodic memory checks, context compression, skill-capture prompts, and pre-write security gates to agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to save conversation summaries and discovered techniques, which can persist sensitive or unwanted content if retention boundaries are unclear. <br>
Mitigation: Require explicit approval before memory or skill writes, avoid storing secrets or personal data, and make saved items reviewable, deletable, and reversible. <br>
Risk: Generated or captured memory content can include prompt-injection text or hidden characters. <br>
Mitigation: Run the documented pre-write security gate before saving content, including checks for prompt-injection patterns, invisible characters, and duplicate entries. <br>


## Reference(s): <br>
- [Hermes Skills on ClawHub](https://clawhub.ai/kofna3369/hermes-skills) <br>
- [Kofna3369 Publisher Profile](https://clawhub.ai/user/kofna3369) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown with inline Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes prompts and procedural checks for memory, context compression, skill tracking, and pre-write security screening.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
