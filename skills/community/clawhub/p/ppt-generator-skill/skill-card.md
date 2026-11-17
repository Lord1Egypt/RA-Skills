## Description:

Generate professional .pptx presentations from topics, uploaded documents, or reference materials, with support for custom PPT templates, local generation, real charts, content chunking, and guided conversation flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuchentsai-design](https://clawhub.ai/user/yuchentsai-design)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to turn written topics, uploaded source materials, or an uploaded .pptx template into a generated presentation file. It guides requirements gathering, analyzes content and templates, validates a slide plan, and produces a finished .pptx locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated presentation plans and rendering steps may expose users to code-execution risk.

Mitigation: Run the skill only in an isolated workspace after validating slide plans and removing the identified JavaScript injection path.

Risk: Skipping validation or accepting loose color values can allow unsafe or malformed presentation inputs.

Mitigation: Keep validation enabled for normal use and enforce strict color and slide-plan validation before generating .pptx files.

Risk: The setup workflow can encourage system-level or global dependency installation.

Mitigation: Use pinned dependencies in a local virtual environment and local npm project; do not run curl-to-sudo commands or global installs on sensitive machines.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yuchentsai-design/skills/ppt-generator-skill)
- [PPT Generator Skill Instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands, JSON slide plans, validation reports, and generated .pptx files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.9+, Node.js, pptxgenjs, markitdown[pptx], pypdf, and python-pptx; optional QA uses LibreOffice and pdftoppm.]

## Skill Version(s):

4.3.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
