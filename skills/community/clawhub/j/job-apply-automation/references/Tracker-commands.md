# Tracker Commands
### job-email-apply / references

These are the exact operations the agent uses to read from and write to
Applications.json. Every operation must follow these formats precisely
to keep the tracker consistent and auditable.

---

## ID Generation

Application IDs are sequential: APP-001, APP-002, APP-003...

Before creating a new entry, read Applications.json and find the highest
existing ID number. Increment by 1. Pad to 3 digits.

If Applications.json has no entries yet, start at APP-001.

Session IDs follow the same pattern: S-001, S-002...

---

## ADD — Log a new application

Triggered: immediately after an application email is sent successfully.

Append this object to the `applications` array in Applications.json:

```json
{
  "id": "APP-[NNN]",
  "date_applied": "[YYYY-MM-DD]",
  "time_applied": "[HH:MM:SS]",
  "company": "[Company name as listed]",
  "role": "[Job title as listed]",
  "platform": "[linkedin | indeed | glassdoor | wellfound | direct | other]",
  "job_url": "[Full URL to the listing]",
  "application_email": "[Email address the application was sent to]",
  "match_score": [0.00],
  "status": "APPLIED",
  "status_history": [
    { "status": "APPLIED", "date": "[YYYY-MM-DD]", "note": "" }
  ],
  "last_updated": "[YYYY-MM-DD]",
  "recruiter_name": "",
  "recruiter_email": "",
  "interview_date": "",
  "interview_time": "",
  "interview_format": "",
  "interview_link": "",
  "salary_listed": "[Value if visible in listing, else empty string]",
  "template_used": "[cold-application | startup-application | referral-application]",
  "skills_targeted": ["[skill1]", "[skill2]", "[skill3]"],
  "cv_attached": true,
  "cv_filename": "cv.pdf",
  "subject_line": "[Exact subject line used]",
  "notes": "",
  "next_action": "Awaiting response"
}
```

After appending, update `_meta.total_applications` and `_meta.last_updated`.

---

## ADD — Log a failed application (no email found)

Triggered: when a qualifying listing is found but no application email
could be located after a reasonable search.

```json
{
  "id": "APP-[NNN]",
  "date_applied": "[YYYY-MM-DD]",
  "time_applied": "[HH:MM:SS]",
  "company": "[Company name]",
  "role": "[Job title]",
  "platform": "[platform]",
  "job_url": "[URL]",
  "application_email": "",
  "match_score": [0.00],
  "status": "EMAIL_NOT_FOUND",
  "status_history": [
    { "status": "EMAIL_NOT_FOUND", "date": "[YYYY-MM-DD]", "note": "Could not locate application email" }
  ],
  "last_updated": "[YYYY-MM-DD]",
  "recruiter_name": "",
  "recruiter_email": "",
  "interview_date": "",
  "interview_time": "",
  "interview_format": "",
  "interview_link": "",
  "salary_listed": "",
  "template_used": "",
  "skills_targeted": [],
  "cv_attached": false,
  "cv_filename": "",
  "subject_line": "",
  "notes": "Searched listing, LinkedIn, and company website. No contact email found.",
  "next_action": "Manual check if interested"
}
```

---

## UPDATE — Change application status

Triggered: when an inbox reply is processed and the status changes.

Find the entry by `id` or by matching `company` + `role`.
Update the `status` field.
Append a new object to `status_history`.
Update `last_updated`.
Update `next_action` to reflect what happens next.

```json
"status": "[NEW_STATUS]",
"status_history": [
  { "status": "APPLIED", "date": "2026-03-21", "note": "" },
  { "status": "[NEW_STATUS]", "date": "[YYYY-MM-DD]", "note": "[Brief note about what triggered this]" }
],
"last_updated": "[YYYY-MM-DD]"
```

Status transitions the agent handles automatically:
- APPLIED → RESPONDED (recruiter replies with interest)
- RESPONDED → INTERVIEW_SCHEDULED (date confirmed)
- APPLIED → REJECTED (rejection email received)
- RESPONDED → REJECTED (rejected after initial contact)
- INTERVIEW_SCHEDULED → INTERVIEW_DONE (date has passed — agent checks dates daily)

Status transitions that require your input:
- INTERVIEW_DONE → OFFER
- INTERVIEW_DONE → REJECTED
- Any → WITHDRAWN (you tell the agent to withdraw)

---

## UPDATE — Add recruiter details

Triggered: when a recruiter replies and their name/email is identifiable.

Find the entry. Update these fields:
```json
"recruiter_name": "[Name from email signature or LinkedIn]",
"recruiter_email": "[Their email address]"
```

---

## UPDATE — Add interview details

Triggered: when an interview is scheduled and confirmed.

```json
"interview_date": "[YYYY-MM-DD]",
"interview_time": "[HH:MM local time]",
"interview_format": "[video | phone | in-person]",
"interview_link": "[Zoom/Meet/Teams URL if provided]",
"next_action": "Prepare for interview [DATE] [TIME]"
```

---

## UPDATE — Add notes

Triggered: when the agent wants to log something for your reference.

Append to the `notes` field. Always prefix with date:
```
"notes": "[YYYY-MM-DD]: [Note text]. [YYYY-MM-DD]: [Additional note]."
```

---

## READ — Duplicate check

Before applying to any listing, check Applications.json:

1. Find all entries where `company` matches (case-insensitive).
2. If a match exists, check `status`.
3. If status is REJECTED or WITHDRAWN, the 60-day cooldown applies —
   check `date_applied`. If more than 60 days ago, OK to apply again.
4. If status is anything else (APPLIED, RESPONDED, INTERVIEW_SCHEDULED,
   INTERVIEW_DONE, OFFER), skip this listing — do not apply.
5. Log the skip reason as DUPLICATE_SKIP in the session summary.

---

## READ — Do-not-apply check

Before applying, check the `do_not_apply` array.
If the company name matches any entry (case-insensitive), skip.
Log reason: "On do-not-apply list."

---

## APPEND — Session log entry

At the end of every session, append to the `session_log` array:

```json
{
  "session_id": "S-[NNN]",
  "date": "[YYYY-MM-DD]",
  "time_start": "[HH:MM:SS]",
  "time_end": "[HH:MM:SS]",
  "applied": [n],
  "skipped_below_threshold": [n],
  "skipped_duplicate": [n],
  "skipped_no_email": [n],
  "inbox_replies_processed": [n],
  "interviews_scheduled": [n],
  "alerts_sent": [n],
  "total_active": [n — count of all entries where status is not REJECTED/WITHDRAWN/OFFER]
}
```

---

## UPDATE — Recalculate stats

After every session, update the `stats` object:

```json
"stats": {
  "total_sent": [count of all APPLIED + all subsequent statuses],
  "total_responded": [count where status_history contains RESPONDED or later],
  "total_interviews": [count where status_history contains INTERVIEW_SCHEDULED],
  "total_offers": [count where status = OFFER],
  "total_rejected": [count where status = REJECTED],
  "response_rate_percent": [total_responded / total_sent * 100, rounded to 1dp],
  "interview_rate_percent": [total_interviews / total_sent * 100, rounded to 1dp],
  "last_calculated": "[YYYY-MM-DD]"
}
```

---

## Data Integrity Rules

- Never delete an entry. Only update status.
- Never overwrite status_history. Only append to it.
- Always write valid JSON. If uncertain, validate before saving.
- The `id` field is immutable once created — never change it.
- `date_applied` and `time_applied` are immutable — they record when
  the email was sent, which is a historical fact.
- If a write fails for any reason, log the failure in the session summary
  and alert the user. Do not silently lose data.
