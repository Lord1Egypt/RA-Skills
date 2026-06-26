---
name: healthcare
description: Use for clinic and healthcare facility operations — patient scheduling, medical records, prescriptions, lab tracking, staff coordination, billing, compliance, and patient communication.
version: "0.1.0"
author: koompi
tags:
  - healthcare
  - clinic
  - patient-scheduling
  - medical-records
  - prescriptions
---

# Healthcare & Clinic Operations Skill

Assist clinics and healthcare facilities with patient management, scheduling, documentation, and operational workflows. Prioritize patient safety, data privacy, and clear communication at all times.

## Heartbeat

When activated during a heartbeat cycle:

1. **Appointments needing confirmation?** Any unconfirmed appointments in the next 48 hours → send reminders
2. **Prescription refills due?** Patients with refills expiring in ≤7 days → flag for provider review and notify patient
3. **Lab results pending?** Results received but not reviewed by provider → alert; results older than 72 hours → escalate
4. **Follow-up visits overdue?** Patients past their scheduled follow-up window → generate outreach list
5. **Staff schedule gaps?** Shifts in next 7 days with no coverage → flag for clinic manager
6. If nothing needs attention → `HEARTBEAT_OK`

## Patient Scheduling

### Appointment Types
- **New patient intake:** 45-60 min. Requires registration, insurance info, medical history forms sent in advance.
- **Follow-up visit:** 15-30 min. Pull prior visit notes and pending orders before appointment.
- **Urgent/walk-in:** Triage immediately. Slot into first available gap or add to overflow.
- **Telehealth:** Confirm patient has link and device access. Send connection instructions 1 hour before.
- **Procedure/lab visit:** Block appropriate time + equipment. Confirm prep instructions sent to patient.

### Scheduling Rules
- No double-booking unless provider explicitly allows overbooking slots
- Buffer 5-10 min between appointments for documentation
- Flag if a provider exceeds daily patient cap
- Keep urgent slots open each day (minimum 2 per provider)
- When rescheduling, offer next 3 available slots

### Appointment Reminders
- 48 hours before: initial reminder (SMS/message preferred, fallback to call)
- 24 hours before: confirmation request — patient must confirm or reschedule
- 2 hours before: final reminder with arrival instructions
- No-show: contact within 1 hour, offer rebooking, log the no-show

## Medical Records & Documentation

### Visit Documentation Structure
```
Patient: [name, ID]
Date: [date] | Provider: [name]
Visit type: [new/follow-up/urgent/telehealth]
Chief complaint: [patient's stated reason]
History of present illness: [details]
Examination findings: [relevant findings]
Assessment: [diagnosis/impression]
Plan: [treatment, prescriptions, referrals, follow-up]
```

### Documentation Principles
- Record at the time of encounter or immediately after — never backfill from memory
- Use objective language: "patient reports..." not "patient claims..."
- Every entry must have date, time, provider name
- Corrections: never delete — append a dated addendum
- Templates speed up documentation but always review before finalizing

### Record Requests
- Verify patient identity before releasing any records
- Log every access and release
- Provide records within the timeframe required by local regulation (default: 30 days)
- Redact information not covered by the request scope

## Prescription Management

### New Prescriptions
- Verify: drug name, dosage, frequency, duration, route
- Check for documented allergies and current medications — flag interactions
- Include clear patient instructions: when to take, with/without food, side effects to watch for
- Log prescribing provider, date, and indication

### Refill Workflow
1. Patient requests refill (message, call, or in-person)
2. Check: last fill date, remaining refills, next appointment date
3. If refills remaining and patient is adherent → process refill
4. If no refills or patient overdue for visit → schedule appointment before refilling
5. Controlled substances: always require provider review, no auto-refills
6. Notify patient when refill is ready for pickup/delivery

### Medication List Maintenance
- Keep an active, accurate medication list per patient
- Reconcile at every visit: add new, remove discontinued, verify doses
- Flag: duplicate therapies, expired prescriptions, medications without a recent review

## Follow-Up Care Coordination

### After Visit
- Schedule follow-up before patient leaves (or within 24 hours for telehealth)
- Send visit summary to patient: diagnosis, medications, next steps, when to return
- Referrals: send within 48 hours, confirm receiving provider has the referral, track status

### Chronic Disease Management
- Maintain a care plan per condition: target metrics, medication, visit frequency, lifestyle goals
- Track key indicators: HbA1c, blood pressure, weight, pain scores — whatever applies
- Alert when a patient misses a monitoring milestone
- Coordinate between specialists — ensure shared care plan is current

### Referral Tracking
```
Patient: [name, ID]
Referring provider: [name]
Referred to: [specialist, facility]
Reason: [indication]
Date sent: [date]
Status: [pending / scheduled / completed / no response]
Follow-up if no response: [date + 7 days]
```

## Lab Results & Test Tracking

### Ordering
- Every lab order needs: test name, indication, ordering provider, urgency level
- Confirm specimen requirements and patient prep instructions
- Send patient prep instructions at time of ordering (fasting, medication holds, etc.)

### Results Workflow
1. Results received → route to ordering provider
2. Provider reviews within 24 hours (critical values: immediately)
3. Normal results → notify patient within 48 hours
4. Abnormal results → provider contacts patient directly, documents discussion and plan
5. Critical results → immediate provider notification + patient contact + document time stamps

### Pending Test Tracker
- Maintain a list of all ordered tests with expected result dates
- Flag overdue results (>3 days past expected)
- Escalate: contact lab if results are late, notify provider

## Staff Scheduling

### Shift Management
- Weekly schedule: provider, nursing, admin, support staff
- Minimum staffing requirements per shift (at least 1 provider + 1 nursing + 1 admin during open hours)
- Flag: overtime approaching limits, consecutive shifts without rest, uncovered shifts
- On-call roster: always have a designated after-hours contact

### Leave & Coverage
- Leave requests: submitted ≥2 weeks in advance for planned leave
- Find coverage before approving leave — never leave a shift unstaffed
- Sick calls: immediately find replacement, notify affected patients if appointments must move
- Track leave balances: annual, sick, continuing education

## Insurance & Billing

### Pre-Visit
- Verify insurance eligibility before appointment
- Check if referral/prior authorization is required — obtain before visit
- Inform patient of estimated out-of-pocket costs when possible

### Post-Visit Billing
- Code visits accurately: diagnosis codes + procedure codes matching documentation
- Submit claims within the payer's filing deadline
- Track claim status: submitted → accepted → paid / denied

### Denied Claims
1. Identify denial reason (coding error, missing auth, eligibility, medical necessity)
2. Correct and resubmit or file appeal within allowed timeframe
3. Log all denials — review monthly for patterns
4. Common fixes: missing modifier, wrong diagnosis code, expired authorization

### Patient Billing
- Send statements within 30 days of service or insurance adjudication
- Itemize charges clearly — patients should understand what they're paying for
- Offer payment plans for balances above a threshold set by the clinic
- Collections: only after 90 days + 3 contact attempts + documented financial hardship screening

## Patient Communication

### Templates
- **Appointment reminder:** Date, time, provider, location, prep instructions, how to reschedule
- **Lab results (normal):** Results summary, "no action needed," next scheduled screening date
- **Lab results (abnormal):** Brief note that provider will call to discuss, do not include raw values in unsecured messages
- **Prescription ready:** Medication name, pickup location, take-as-directed reminder
- **Missed appointment:** Reschedule prompt, note that continuity of care matters
- **Referral update:** Specialist name, date, location, what to bring
- **Balance due:** Amount, due date, payment options, contact for questions

### Communication Rules
- Never include detailed diagnoses, test values, or sensitive information in unsecured messages
- Always identify the clinic and provide a callback number
- Respond to patient inquiries within 1 business day
- Urgent clinical questions → route to provider, not administrative staff
- Use plain language — no medical jargon in patient-facing messages

## Compliance & Privacy

### Core Privacy Principles
- **Minimum necessary:** Only access or share the minimum information needed for the task
- **Need to know:** Staff access records only for patients they are actively treating or supporting
- **Patient consent:** Obtain consent before sharing records with third parties (except where legally required)
- **Audit trail:** Log every access, modification, and disclosure of patient records
- **De-identification:** Remove names, IDs, dates of birth, and other identifiers when using data for reporting or analysis

### Operational Safeguards
- Lock screens when unattended. Auto-lock after 5 minutes of inactivity.
- Never discuss patient information in public areas
- Verify identity before disclosing any information by phone or message
- Shred physical documents containing patient information
- Report any suspected breach immediately to the clinic's privacy officer

### Retention
- Retain records for the period required by local regulation (default minimum: 7 years for adults, until age of majority + 7 years for minors)
- Secure destruction after retention period — document the destruction

## Emergency Escalation

### Triage Priority
- **Immediate (red):** Life-threatening — chest pain, difficulty breathing, severe bleeding, loss of consciousness → call emergency services, do not wait
- **Urgent (orange):** Needs same-day attention — high fever, acute pain, worsening symptoms → provider assessment within 1 hour
- **Semi-urgent (yellow):** Needs attention within 24-48 hours — persistent symptoms, medication reactions, post-procedure concerns → schedule urgent visit
- **Routine (green):** Standard scheduling — chronic management, preventive care, refills

### Escalation Protocol
1. Identify severity using triage categories above
2. Immediate → call emergency services + notify on-site provider + document time of identification and actions taken
3. Urgent → pull patient chart, alert provider, prepare exam room
4. Document every escalation: who identified, when, what action, outcome
5. Post-event review for all immediate and urgent cases within 48 hours

### After-Hours
- Route to on-call provider for urgent/immediate concerns
- Non-urgent → acknowledge receipt, schedule next-day follow-up
- Always provide emergency service contact info in after-hours messages
