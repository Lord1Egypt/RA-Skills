## Description: <br>
Lark is a digital command center skill that helps agents diagnose coordination friction and orchestrate chat, approvals, meetings, docs, spreadsheets, calendars, and related communication with tact. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AGIsearch](https://clawhub.ai/user/AGIsearch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Managers, project owners, and cross-functional operators use this skill to turn Lark workspace activity into prioritized briefings, action items, reminder drafts, meeting follow-through, status checks, and coordination recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can work with sensitive workplace context across messages, approvals, documents, spreadsheets, calendars, and meetings. <br>
Mitigation: Install it with a dedicated least-privilege Lark app and grant only the scopes needed for the intended workflow. <br>
Risk: Routine write actions such as messages, spreadsheet edits, scheduling changes, and approval handling can affect teams or senior stakeholders. <br>
Mitigation: Keep Counselor Mode unless write access is intentional, and require explicit confirmation for sends, edits, approvals, scheduling changes, and high-sensitivity communication. <br>
Risk: Incomplete context can lead to misleading summaries, premature nudges, or action on stale information. <br>
Mitigation: Review the surfaced context and recommendations before acting, and fall back to suggestion mode when authorization, permissions, or context are insufficient. <br>


## Reference(s): <br>
- [Lark on ClawHub](https://clawhub.ai/AGIsearch/lark) <br>
- [AGIsearch Publisher Profile](https://clawhub.ai/user/AGIsearch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown briefings, ranked lists, drafts, recommendations, and action summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LARK_APP_ID and LARK_APP_SECRET through the host platform connector; high-sensitivity write actions should remain confirmation-gated.] <br>

## Skill Version(s): <br>
2.0.1 (source: release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
