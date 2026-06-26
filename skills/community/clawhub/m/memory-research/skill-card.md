## Description: <br>
Research an external subject using web search, synthesize findings into a structured Basic Memory entity. Use when asked to research a company, person, technology, or topic, or when a bare name or URL is provided that implies a research request. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phernandez](https://clawhub.ai/user/phernandez) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge-base users use this skill to research public companies, people, technologies, or topics, compare findings with existing Basic Memory notes, and propose structured memory entries or updates with sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public web research can capture outdated, incomplete, or misleading information. <br>
Mitigation: Review the cited sources and the proposed note content before approving a Basic Memory write or update. <br>
Risk: A bare name or URL can be interpreted as a research request when the user did not intend persistent follow-up. <br>
Mitigation: Be explicit when a name or URL is only contextual and should not trigger research or note creation. <br>
Risk: Approved notes can retain sensitive personal or business context supplied during the request. <br>
Mitigation: Avoid approving storage of sensitive context unless retention in Basic Memory is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/phernandez/memory-research) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown research summaries with source lists and Basic Memory write/edit call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Proposes note creation or updates only after user approval.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
