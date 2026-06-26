## Description: <br>
Transforms rough concepts and supporting inputs into structured, copy-ready LLM prompts using prompt-engineering frameworks and quality checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[subaru0573](https://clawhub.ai/user/subaru0573) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, prompt engineers, and other external users use this skill to turn vague or multimodal task ideas into refined LLM prompts. It guides clarification, selects an appropriate prompting framework, and returns a final prompt suitable for copying into another model or agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated prompts can include inappropriate visible-reasoning instructions for sensitive tasks. <br>
Mitigation: Ask for concise justification or brief rationale instead of full hidden reasoning when using the generated prompt in sensitive work. <br>
Risk: The workflow may ask users to provide documents, links, images, or other sensitive source material. <br>
Mitigation: Avoid supplying confidential inputs unless the host agent and enabled tools are trusted for that data. <br>
Risk: The final prompt quality depends on the user's clarifying answers and selected framework. <br>
Mitigation: Review the final prompt against the included quality criteria before using it in production workflows. <br>


## Reference(s): <br>
- [Prompt Engineering Frameworks](references/frameworks.md) <br>
- [Prompt Quality Criteria](references/quality-criteria.md) <br>
- [Prompt Templates](references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown with a fenced code block for the final prompt and a brief framework explanation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask 5-10 clarifying questions and may produce final prompts in English or Arabic based on user choice.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
