# The nudge

At most one Slack post a day, only when something is due. Grouped by owner, overdue first.

```text
:hourglass: *Next steps due — <weekday> <date>*
*<owner>*
• <account>: "<promise, quoted>" — <you promised | they promised> on <call date>, due <due date> (<n> days overdue | today). <what would close it>
_Sources: <every source entry path>_
```

## Rules for each line

- **The promise is quoted** from the call entry's Actions or body. A paraphrase is how a rep gets
  chased for something nobody said.
- **Who promised** decides the verb. "You promised" is a task. "They promised" is a follow-up to
  chase; the line says there is nothing to do for them.
- **What would close it** names the evidence the tracker will look for tomorrow: an email, a meeting,
  a note, a task. A rep who does the thing without it being logged keeps getting the nudge, and the line
  tells them why.
- **Sources** lists every call entry the post relied on.

A row leaves the post when it closes on evidence or when a human sets its status to `dropped` in the
`commitments` model.
