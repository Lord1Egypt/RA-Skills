## Description: <br>
Process unstructured external input (meeting transcripts, conversation logs, pasted documents) into structured Basic Memory entities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phernandez](https://clawhub.ai/user/phernandez) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to convert pasted meetings, conversations, documents, articles, and email threads into structured Basic Memory notes. It helps preserve source material, identify entities, propose new knowledge graph entries for approval, and capture follow-up actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pasted source material may contain secrets, regulated data, or private meeting details that would be retained in Basic Memory. <br>
Mitigation: Redact sensitive content before ingestion and install the skill only when persistent Basic Memory storage is intended. <br>
Risk: Optional web research could expose private context if used for confidential meetings, emails, projects, or relationships. <br>
Mitigation: Skip optional web research for private material and rely on the provided source content unless the user explicitly approves external research. <br>
Risk: Automatically created entities could add inaccurate or unwanted knowledge graph entries. <br>
Mitigation: Review proposed notes and entity proposals before approval, and keep the skill's approval step for new entities. <br>


## Reference(s): <br>
- [Memory Ingest on ClawHub](https://clawhub.ai/phernandez/memory-ingest) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown with structured note examples and inline code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces proposed Basic Memory note content, entity proposals, observations, relations, and action item summaries; new entities require user approval before creation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
