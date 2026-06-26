---
name: new-job-first-week-admin-board
displayName: "New Job First-Week Admin Board"
version: "1.0.0"
description: "Create a first-week new-job admin board for access requests, forms, equipment, meetings, questions, deadlines, blockers, and follow-ups while avoiding passwords, identity numbers, payroll details, and sensitive HR data."
triggerKeywords:
  - new job first week
  - first week admin board
  - new employee checklist
  - onboarding admin checklist
  - first week work setup
  - access request tracker
  - new hire equipment checklist
  - onboarding questions board
  - first week deadlines
  - job start logistics
tags:
  - onboarding
  - admin
  - workplace
  - checklist
  - logistics
license: "MIT-0"
language: "en"
hasExecutableCode: false
promptOnly: true
execution: "noExec"
---

# New Job First-Week Admin Board

## Purpose

Use this prompt-only skill when a user is starting a new job, internship, contract, rotation, transfer, or team placement and wants the first-week logistics under control. The deliverable is a practical board for access, forms, equipment, meetings, contacts, questions, blockers, deadlines, and follow-ups.

This is an organization workflow only. It must not collect, store, expose, or reproduce passwords, one-time codes, identity numbers, tax IDs, Social Security numbers, bank details, payroll details, medical details, immigration details, background-check details, or sensitive HR data.

## Privacy Boundary

Do not ask the user to paste passwords, passcodes, recovery codes, full IDs, tax forms, bank numbers, offer letters with private compensation, medical accommodation details, background-check details, immigration documents, home address, date of birth, or other sensitive HR data.

When an admin item involves sensitive data, track only safe metadata, such as document type, owner, deadline, status, and where the user should handle it securely. Use placeholders like `complete in HR portal`, `confirm with HR`, `bring ID in person`, or `store in password manager` instead of recording the sensitive value.

Do not advise bypassing company security, sharing credentials, using personal email for confidential work, forwarding internal documents without permission, or storing work secrets in the board.

## Best Inputs

Ask for safe logistics details:

- Start date, work mode, location, time zone, manager, onboarding buddy, recruiter, HR contact, IT contact, or team alias.
- Known first-week schedule, meetings, orientation blocks, training sessions, and deadlines.
- Equipment expected, such as laptop, badge, phone, headset, monitor, keyboard, security key, parking pass, uniform, or tools.
- Systems or access categories needed, such as email, chat, calendar, VPN, HR portal, ticketing, repository, design tool, CRM, finance tool, or learning platform.
- Forms by category and status only, such as tax form, direct deposit, benefits, emergency contact, policy acknowledgement, compliance training, or background step.
- Questions the user wants to ask without including private data.
- Constraints such as commute, childcare, accessibility, remote setup, time zones, dress code, cafeteria, parking, or building access.

If the user provides sensitive details, do not repeat them. Replace them with safe placeholders and continue with the board.

## Workflow

1. **Set privacy rules.** State that the board tracks status and next actions only, not passwords, IDs, bank details, or sensitive HR data.
2. **Collect safe context.** Gather start date, work mode, contacts, schedule, equipment, access categories, form categories, deadlines, and known blockers.
3. **Create first-week lanes.** Sort items into Before Day 1, Day 1, Days 2-3, Days 4-5, Waiting On, Questions, and Done.
4. **Track access safely.** Record system name, request owner, request status, due date, verification step, and support contact. Never record credentials, one-time codes, recovery codes, or secret links.
5. **Track forms safely.** Record form category, portal or secure location, deadline, status, and who can help. Do not record form contents or sensitive values.
6. **Track equipment and workspace.** List item, owner, pickup or shipping status, setup action, return or receipt note, and blocker.
7. **Map meetings and deadlines.** Add time, topic, prep needed, question to ask, and follow-up owner.
8. **Flag blockers.** Mark anything that prevents work, such as missing badge, laptop, VPN, manager invite, payroll portal access, or unclear training deadline.
9. **Draft questions.** Create concise questions for HR, manager, IT, buddy, facilities, payroll, benefits, or security without including private details.
10. **Produce the board.** Return a copy-ready artifact the user can maintain during the first week.

## Output Format

Return the board in this order.

### 1. Privacy Note

Start with a short note: this board tracks status, owners, deadlines, and questions only. It must not contain passwords, passcodes, full IDs, bank details, tax values, medical details, immigration details, background-check details, or sensitive HR data.

### 2. First-Week Snapshot

| Field | Detail |
|---|---|
| Start date | |
| Work mode/location | |
| Manager | |
| Buddy or point person | |
| HR contact | |
| IT contact | |
| Main first-week goal | |
| Known deadlines | |
| Assumptions | |

Use role names or initials if privacy is a concern.

### 3. Board Lanes

| Lane | Item | Owner | Due date | Status | Next action | Safe note |
|---|---|---|---|---|---|---|
| Before Day 1 | | | | | | |
| Day 1 | | | | | | |
| Days 2-3 | | | | | | |
| Days 4-5 | | | | | | |
| Waiting On | | | | | | |
| Questions | | | | | | |
| Done | | | | | | |

Status options: Not started, Requested, Waiting, Scheduled, In progress, Blocked, Confirmed, Done, Not needed.

### 4. Access Tracker

| System or access category | Why needed | Request owner | Status | Verification step | Deadline | Support path |
|---|---|---|---|---|---|---|
| Email/calendar | | | | | | |
| Chat | | | | | | |
| HR portal | | | | | | |
| VPN/security tool | | | | | | |
| Team tools | | | | | | |

Do not include passwords, one-time codes, recovery codes, secret URLs, tokens, or account numbers.

### 5. Forms and HR Tasks

| Category | Secure place to complete | Owner/contact | Due date | Status | Question or blocker |
|---|---|---|---|---|---|
| Tax form | HR portal or official process | | | | |
| Direct deposit | HR/payroll portal or official process | | | | |
| Benefits | HR portal or official process | | | | |
| Emergency contact | HR portal or official process | | | | |
| Policy acknowledgement | Company system | | | | |
| Training | Learning system | | | | |

Track categories and status only. Do not record private values.

### 6. Equipment and Workspace

| Item | Owner | Pickup/ship/setup step | Status | Blocker | Follow-up |
|---|---|---|---|---|---|
| Laptop | | | | | |
| Badge/access card | | | | | |
| Phone/headset | | | | | |
| Monitor/keyboard/mouse | | | | | |
| Security key | | | | | |
| Workspace/desk/locker | | | | | |

### 7. Meetings, Training, and Prep

| Day/time | Meeting or training | Prep needed | Question to ask | Follow-up owner | Done |
|---|---|---|---|---|---|
| | | | | | |

### 8. Questions to Ask

Group questions by owner:

- Manager:
- Onboarding buddy:
- HR:
- IT/security:
- Facilities:
- Payroll/benefits:
- Team/project owner:

Keep questions specific and safe. Use placeholders when sensitive topics are involved, such as `Where should I complete the payroll setup securely?`

### 9. Blocker Escalation List

| Blocker | Impact | Since | Owner | Next follow-up | Escalation path |
|---|---|---|---|---|---|
| | | | | | |

Escalate politely when a blocker prevents work, access, pay setup, required training, building entry, or essential communication.

### 10. End-of-Week Reset

```text
FIRST-WEEK RESET
[ ] Confirm required forms are submitted through official systems
[ ] Confirm core access works without storing credentials in this board
[ ] Confirm equipment is received and usable
[ ] Move unresolved blockers to next week
[ ] Send manager or buddy question list
[ ] Save safe notes in the approved work location
[ ] Remove any sensitive information accidentally added
```

## Style

- Be calm, practical, and deadline-oriented.
- Make the board easy to scan during a busy first week.
- Use safe placeholders instead of sensitive data.
- Prefer owner, status, and next action over long explanations.
- Make blockers visible without making the user sound demanding.
- Respect remote, hybrid, onsite, intern, contractor, hourly, salaried, and union or regulated workplace contexts.

## Quality Bar

A strong result helps the user know what to do next, who owns each item, what is blocked, and what questions to ask. It must reduce first-week chaos without becoming a place where private HR data or credentials are stored.

## Example Prompts

- "Build a first-week admin board for my new job starting Monday."
- "Track my access requests, forms, and equipment so nothing falls through the cracks."
- "Create a questions list for HR, IT, and my manager before my first day."
