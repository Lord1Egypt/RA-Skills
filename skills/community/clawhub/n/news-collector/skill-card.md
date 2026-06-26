## Description: <br>
Personalized news briefing generation skill that supports on-demand one-time briefings or recurring updates across search, filtering, organization, and output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[winsaney](https://clawhub.ai/user/winsaney) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to turn a topic, source preference, cadence, and output preference into a structured news or information briefing. It supports both immediate research briefings and recurring newsletter-style workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Briefings may include incorrect, low-quality, or insufficiently sourced information if source selection and filtering are weak. <br>
Mitigation: Prefer high-quality, relevant sources, require source names and links in outputs, and review briefings before relying on them. <br>
Risk: Configuring private sources or delivery through email, chat, webhooks, or other services can introduce credential and data-exposure risks. <br>
Mitigation: Review credentials, private-source access, and delivery settings separately before enabling those integrations. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/winsaney/news-collector) <br>
- [Basic briefing template](assets/template-basic.md) <br>
- [Advanced newsletter template](assets/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown or plain text briefing with source links and optional reusable templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce one-time briefings, recurring briefing workflows, source lists, column structures, and customized briefing templates.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
