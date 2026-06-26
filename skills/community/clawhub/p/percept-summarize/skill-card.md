## Description: <br>
Generates AI summaries of conversations after silence, extracting entities, action items, and relationships for searchable meeting notes and context retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jarvis563](https://clawhub.ai/user/jarvis563) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to turn recent conversation transcripts into searchable summaries, action items, entity records, and relationship context for follow-up and recall. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation transcripts and derived summaries may contain sensitive personal or business information and are processed by OpenClaw. <br>
Mitigation: Confirm consent, review whether OpenClaw sends prompts to a remote model, and enable the skill only where that processing is acceptable. <br>
Risk: Summaries, entities, relationships, and speaker profiles are stored locally and may be accessible through the dashboard or SQLite data. <br>
Mitigation: Restrict access to the dashboard and database, review retention needs, and define a deletion process for stored conversation-derived records. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jarvis563/percept-summarize) <br>
- [Percept GitHub repository](https://github.com/GetPercept/percept) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown and text, with optional SQL snippets for querying stored summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Conversation-derived summaries, entities, relationships, and speaker profiles may be retained locally according to the artifact's retention periods.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
