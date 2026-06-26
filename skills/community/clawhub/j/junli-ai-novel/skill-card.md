## Description: <br>
A Chinese long-form web novel writing assistant for project setup, chapter continuation, targeted revision, project memory maintenance, longform governance, chapter review, and commercial packaging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ljunn](https://clawhub.ai/user/ljunn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External authors and agent users use this skill to plan, continue, revise, govern, review, and package serialized Chinese web novels while preserving project memory, chapter intent, character records, timeline continuity, and longform structure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read sensitive outlines, character notes, timelines, prior chapters, and other local project writing files. <br>
Mitigation: Install and use it only in novel project directories where that level of local file access is acceptable. <br>
Risk: The skill may update project memory, governance, runtime, progress, or review files that affect future story-state decisions. <br>
Mitigation: Use explicit project paths and review generated or modified governance and runtime files before relying on them for important continuity decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ljunn/junli-ai-novel) <br>
- [Project workflow entrypoint](PROJECT.md) <br>
- [Skill operating instructions](SKILL.md) <br>
- [Chapter workflow](references/chapter-workflow.md) <br>
- [Chapter writing guide](references/chapter-guide.md) <br>
- [Quality checklist](references/quality-checklist.md) <br>
- [Longform governance protocol](references/longform-governance.md) <br>
- [Style and risk guardrails](references/style-guardrails.md) <br>
- [Rule-based text checks](references/rule-linting.md) <br>
- [Commercial packaging and marketing brief](references/marketing.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, plain text, JSON-like reports, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local novel project files, runtime planning files, progress logs, review reports, and governance documents.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
