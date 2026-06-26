---
name: hipaa-patient-comms
version: 1.0.0
description: "Draft patient-facing communications (appointment reminders, billing notices, follow-ups, recall messages) that avoid HIPAA violations. Flags risky language, strips PHI from drafts, and follows minimum necessary standard."
triggers:
  - patient email
  - patient reminder
  - appointment reminder
  - patient follow up
  - patient communication
  - hipaa compliant
  - medical billing notice
  - patient recall
  - dental reminder
  - clinic email
  - healthcare communication
  - patient outreach
tools:
  - read_file
  - write_file
metadata:
  openclaw:
    emoji: "🏥"
    homepage: https://gaffneyits.com/openclaw
    os: ["darwin", "linux", "win32"]
    autostart: false
    tags:
      - healthcare
      - hipaa
      - medical
      - dental
      - patient-communication
      - compliance
      - appointment
      - billing
---

# HIPAA Patient Comms

Draft patient-facing communications for medical, dental, and therapy practices that follow HIPAA safe-harbor guidelines. Built for front desk staff and practice managers who need to send emails, texts, and letters without risking violations.

## When to Use This Skill

Use when the user asks to:
- Write a patient appointment reminder
- Draft a billing notice for a patient
- Create a follow-up message after a visit
- Write a recall/reactivation message for lapsed patients
- Send a patient any communication from a healthcare practice
- Check if a patient message is HIPAA compliant

## HIPAA Rules This Skill Enforces

### The Minimum Necessary Standard
Only include the minimum information needed for the communication's purpose. A reminder needs a date and time — not a diagnosis.

### What NEVER Goes in Patient Communications (PHI)
These must NEVER appear in emails, texts, or unsecured messages:

| Prohibited | Why |
|-----------|-----|
| Diagnosis or condition name | "Your diabetes follow-up" reveals a condition |
| Treatment details | "Your chemotherapy session" reveals treatment |
| Medication names | "Your Metformin refill" reveals a condition |
| Test results | "Your lab results are normal" — any results |
| Provider specialty (if revealing) | "Your oncology appointment" implies cancer |
| Insurance claim details | Claim numbers, denial reasons |
| Full date of birth | Combined with name = identifier |
| SSN, MRN (medical record number) | Direct identifiers |
| Photos or images of the patient | Biometric identifiers |

### What IS Safe in General Communications
| Safe | Example |
|------|---------|
| First name only | "Hi Sarah" |
| Appointment date and time | "Tuesday March 25 at 2:00 PM" |
| Practice name and address | "Main Street Family Practice" |
| Generic purpose | "your upcoming appointment" (not "your cardiology appointment") |
| Office phone number | For the patient to call back |
| Patient portal link | "Log in to your patient portal for details" |
| Generic follow-up | "We'd love to see you for a visit" (not "time for your annual mammogram") |

## Communication Types

### 1. Appointment Reminder

**Collect:**
- patient_first_name (required)
- appointment_date (required)
- appointment_time (required)
- practice_name (required)
- practice_phone (required)
- practice_address (optional)
- provider_name (optional — use only first name + last initial or "your provider")
- portal_link (optional)

**Rules:**
- NEVER mention the type of appointment, specialty, or reason for visit
- Use "your appointment" or "your upcoming visit" — nothing more specific
- Include a way to confirm, reschedule, or cancel
- Keep under 100 words for email, under 160 characters for text

**Template — Email:**
```
Subject: Appointment Reminder — {{practice_name}}

Hi {{patient_first_name}},

This is a reminder that you have an appointment on {{appointment_date}} at {{appointment_time}} at {{practice_name}}.

Please arrive 15 minutes early. If you need to reschedule or cancel, call us at {{practice_phone}}.

See you soon!
{{practice_name}}
```

**Template — SMS:**
```
Hi {{patient_first_name}}, reminder: you have an appointment on {{appointment_date}} at {{appointment_time}}. To reschedule, call {{practice_phone}}. — {{practice_name}}
```

### 2. Billing Notice

**Collect:**
- patient_first_name (required)
- balance_amount (required)
- practice_name (required)
- practice_phone (required)
- payment_link or portal_link (optional)
- statement_date (optional)

**Rules:**
- NEVER mention what the charge was for (no procedure names, codes, or visit types)
- Say "your account" or "your balance" — not "your surgery balance"
- Direct them to the portal or phone for details
- Offer to discuss payment options

**Template — Email:**
```
Subject: Account Balance Notice — {{practice_name}}

Hi {{patient_first_name}},

Our records show a balance of {{balance_amount}} on your account with {{practice_name}}.

For details or to make a payment, please log in to your patient portal or call us at {{practice_phone}}.

If you have questions about your balance or need to discuss payment options, we're happy to help.

Thank you,
{{practice_name}}
```

### 3. Post-Visit Follow-Up

**Collect:**
- patient_first_name (required)
- visit_date (required)
- practice_name (required)
- practice_phone (required)
- portal_link (optional)

**Rules:**
- NEVER mention what was discussed, diagnosed, or treated
- Say "your recent visit" — nothing more specific
- Direct them to the portal for visit summaries, results, or instructions
- Can ask generally about their experience

**Template — Email:**
```
Subject: Thank You for Your Visit — {{practice_name}}

Hi {{patient_first_name}},

Thank you for visiting {{practice_name}} on {{visit_date}}. We hope your experience was positive.

If you have any questions or concerns following your visit, please don't hesitate to call us at {{practice_phone}} or log in to your patient portal.

Take care,
{{practice_name}}
```

### 4. Recall / Reactivation

**Collect:**
- patient_first_name (required)
- practice_name (required)
- practice_phone (required)
- months_since_visit (optional)
- scheduling_link (optional)

**Rules:**
- NEVER mention what type of visit they're overdue for
- Say "it's been a while since your last visit" — not "you're overdue for a cleaning" or "time for your annual physical"
- Keep the tone warm and inviting, not guilt-inducing
- Provide an easy way to schedule

**Template — Email:**
```
Subject: We Miss You! — {{practice_name}}

Hi {{patient_first_name}},

It's been a while since your last visit to {{practice_name}}, and we'd love to see you again.

If you'd like to schedule an appointment, give us a call at {{practice_phone}} or book online.

We look forward to hearing from you!
{{practice_name}}
```

## HIPAA Compliance Check Mode

If the user asks to "check" or "review" an existing message, analyze it using this process:

1. **Scan for PHI violations.** Look for any of the prohibited items listed above.
2. **Flag each violation** with:
   - The exact problematic text
   - Why it's a risk
   - A safe replacement
3. **Output format:**

```
**HIPAA Compliance Review**

🔴 **VIOLATION:** "[problematic text]"
   Risk: [explanation]
   Fix: [safe replacement]

🟡 **WARNING:** "[borderline text]"
   Risk: [explanation]
   Suggestion: [safer alternative]

✅ **CLEAR** — No additional issues found.

**Corrected Version:**
[full corrected message]
```

## Stop Conditions

- Do NOT generate if the user wants to include diagnosis, treatment, or condition information in an unsecured communication. Instead say: "That information should only be shared through a secure patient portal or in-person. I can help you write a message that directs the patient to their portal."
- Do NOT provide legal advice about HIPAA. Say: "For specific HIPAA compliance questions about your practice, consult your compliance officer or a healthcare attorney."
- Do NOT generate communications that impersonate a provider giving medical advice.
- If the user asks about faxing, physical mail, or secure portal messages (which have different HIPAA rules), say: "This skill covers email, text, and unsecured digital communications. Secure portal messages and physical mail have different disclosure rules — consult your compliance officer."
