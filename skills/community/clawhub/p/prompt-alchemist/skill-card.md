## Description: <br>
Prompt Alchemist helps agents diagnose and rewrite user prompts with a four-part distillation workflow that improves structure, clarity, and expected answer quality. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cherish133](https://clawhub.ai/user/cherish133) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
AI users, writers, developers, and prompt engineers use this skill to turn rough prompts into clearer, task-appropriate prompts. It provides diagnostics, quality ratings, structured rewrites, and concise guidance for prompt refinement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation wording may cause the skill to respond to pasted prompt-like text when the user did not intend prompt optimization. <br>
Mitigation: Invoke the skill when the user clearly asks for prompt rewriting, diagnosis, or improvement, and avoid using it as the default handler for arbitrary pasted content. <br>
Risk: Prompt rewrites can change user intent or remove important constraints if the optimized version is accepted without review. <br>
Mitigation: Review the rewritten prompt against the original request, especially any explicit constraints, tone requirements, and safety boundaries, before using it. <br>


## Reference(s): <br>
- [Source repository](https://github.com/Cherish133/prompt-alchemist) <br>
- [ClawHub skill page](https://clawhub.ai/cherish133/skills/prompt-alchemist) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown with structured prompt snippets and XML-style prompt templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs vary by task complexity, from brief diagnostics plus a rewritten prompt to a fuller optimization report.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
