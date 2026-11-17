## Description:

Route meeting notes, transcripts, Feishu docs, wiki pages, or minutes links into concrete execution channels for post-meeting follow-through, including action extraction, owner assignment, Feishu updates, Bitable tracking, follow-up messages, reminders, and delegated agent work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaonizhou-crypto](https://clawhub.ai/user/xiaonizhou-crypto)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and operators use this skill to turn meeting notes, transcripts, Feishu documents, wiki pages, or minutes links into approved, trackable next steps. It helps prepare routing plans, draft follow-ups, update shared artifacts, create reminders, and hand off deeper work after user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Proposed routes could send messages, create many tracker records, or pass meeting context onward before the user has checked them.

Mitigation: Present a compact routing plan first and execute only the batches the user explicitly approves.

Risk: Unclear owners, destinations, table identifiers, or chat targets could cause follow-up actions to go to the wrong place.

Mitigation: Surface missing inputs under needs-your-choice items and draft the next-best artifact when direct execution is blocked.

Risk: Delegating meeting context to another agent session can expose more context than the task needs.

Mitigation: Keep delegated tasks narrow, include only relevant meeting context, state the required output, and require the delegated session to report back before marking work complete.

## Reference(s):

- [Routing Rules](artifact/references/routing-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown routing plans, drafted messages, doc-ready sections, tracker schema proposals, reminder text, and delegated task briefs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user approval before executing routed actions such as messages, record creation, reminders, or delegated work.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
