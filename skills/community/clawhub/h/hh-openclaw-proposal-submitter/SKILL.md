---
name: hh-openclaw-proposal-submitter
description: Review HH.ru application packets for clarity, consent, and public-safe wording before a human submits them.
---

# HH Application Packet Reviewer

Use this skill to prepare and review an HH.ru application packet. Keep the work
to drafting, applicant-facing wording, and a final human-submission checklist.

## Inputs

Collect:

- vacancy URL and title,
- employer name,
- resume title or role fit summary,
- applicant contact preference,
- draft cover letter,
- optional attachment list,
- user-approved submission intent.

Do not request or store account passwords, session cookies, recovery data, or
private employer chat content.

## Review Workflow

1. Summarize the target role and applicant fit in one paragraph.
2. Check the cover letter for:
   - accurate role and company references,
   - no invented experience,
   - no hidden scoring, workflow notes, or private rationale,
   - clear human approval before submission.
3. Produce a final packet with:
   - role summary,
   - reviewed cover letter,
   - attachments checklist,
   - submit/no-submit decision,
   - exact remaining questions for the human.

## Output

Return:

- reviewed application packet,
- risk notes,
- final human-submission checklist,
- concise final message text only if the user asked for it.

## Guardrails

- Do not perform live submission.
- Do not automate account login, captcha, 2FA, or browser actions.
- Do not imply employer contact has happened unless the user confirms it.
- Keep applicant-facing text limited to what the employer should see.
