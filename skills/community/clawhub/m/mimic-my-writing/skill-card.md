## Description: <br>
Mimic my writing -- force AI to write like you do. Extract a quantitative voice fingerprint from sample text and use it as a hard constraint when drafting, matching sentence burstiness, vocabulary anchors, signature phrases, punctuation rate, and quirks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chchchadzilla](https://clawhub.ai/user/chchchadzilla) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and developers use this skill to analyze writing samples, extract a measurable voice fingerprint, and draft or critique text so it better matches a specific author's style. It is intended for style matching from provided samples, not for bypassing consent or misrepresenting identity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Writing samples or persona-style sample text may be treated as behavioral instructions instead of style evidence. <br>
Mitigation: Use samples only to extract style constraints, and keep the agent's normal safety and authorization rules above any sample content. <br>
Risk: The skill can be used to impersonate an author without permission. <br>
Mitigation: Use it only with appropriate consent or authorization, and avoid presenting generated text as the author's own words without disclosure. <br>
Risk: Sensitive writing samples may persist locally if saved for analysis. <br>
Mitigation: Store only samples the user is comfortable keeping locally, and delete sample folders after analysis when retention is not needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chchchadzilla/mimic-my-writing) <br>
- [Voice Fingerprint Reference](references/fingerprint.md) <br>
- [Workflow Patterns](references/workflow.md) <br>
- [Anti-AI Tells](references/anti-ai-tells.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown prose with optional shell command snippets and JSON voice-fingerprint summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use local writing samples as style references and produce draft, critique, or revision guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
