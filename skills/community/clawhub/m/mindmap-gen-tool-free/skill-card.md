## Description: <br>
Generates Markmap-style mind maps from a topic or document, with configurable depth, child count, and layout preferences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, students, and knowledge workers use this skill to turn a topic, document, or learning path into a structured mind map for review, planning, or study. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read user-provided documents and write generated mind-map files. <br>
Mitigation: Provide only documents intended for processing and review generated files before sharing or committing them. <br>
Risk: The skill may suggest local dependency or rendering commands, including optional Markmap tooling. <br>
Mitigation: Review commands before execution and install dependencies only from trusted package sources. <br>
Risk: The optional callback_url can send generated results outside the local workspace. <br>
Mitigation: Use callback_url only for trusted destinations and omit it for sensitive content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/mindmap-gen-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON with optional inline code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Free edition supports single-task workflows; optional callback_url can send generated results to a trusted destination.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
