## Description: <br>
Write, test, and iterate prompts for AI models with voice preservation, model-specific adaptation, and systematic failure analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, content teams, and AI practitioners use this skill to draft, adapt, test, and refine prompts across models while preserving voice and diagnosing prompt failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local prompt memory can retain sensitive writing samples, preferences, corrections, or project details in ~/prompting/. <br>
Mitigation: Keep secrets, regulated data, proprietary writing samples, and sensitive personal details out of memory.md and history.md; inspect or delete those files periodically. <br>


## Reference(s): <br>
- [Prompt Failure Modes](artifact/failures.md) <br>
- [Prompt Iteration Workflow](artifact/iteration.md) <br>
- [Prompting Memory Setup](artifact/memory-template.md) <br>
- [Model-Specific Quirks](artifact/models.md) <br>
- [Advanced Prompting Techniques](artifact/techniques.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with occasional shell commands and prompt examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local prompt memory files under ~/prompting/.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
