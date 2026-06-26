## Description: <br>
Convert meeting notes or transcripts into clear summaries, decisions, and action items with owners and due dates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codedao12](https://clawhub.ai/user/codedao12) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external collaborators, and operators use this skill to turn meeting transcripts or detailed notes into summaries, decisions, action items, open questions, and draft recap messages for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting transcripts and participant lists may contain confidential information. <br>
Mitigation: Treat meeting content as confidential and avoid sharing outputs outside the user's context. <br>
Risk: Generated owners, due dates, or commitments may be inferred from incomplete notes. <br>
Mitigation: Mark inferred owners or due dates as tentative and require user review before using the follow-up package. <br>
Risk: Calendar, task, or messaging integrations could change external systems if used without review. <br>
Mitigation: Use draft modes only and require explicit user confirmation before any task, calendar, or message action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/codedao12/meeting-to-action) <br>
- [Overview](references/overview.md) <br>
- [UX](references/ux.md) <br>
- [Safety](references/safety.md) <br>
- [Auth](references/auth.md) <br>
- [Endpoints](references/endpoints.md) <br>
- [Webhooks](references/webhooks.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Drafts only; does not create tasks, calendar invites, or send messages automatically.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
