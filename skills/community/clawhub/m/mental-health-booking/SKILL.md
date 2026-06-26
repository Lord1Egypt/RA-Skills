---
name: mental-health-booking
description: >
  Book same-day psychiatric and mental health telehealth appointments through conversation — no forms, no portals.
  Covers ADHD, anxiety, depression, insomnia, OCD, PTSD, and narcolepsy across 51 US states.
  Connects you with board-certified providers from curated telehealth platforms including Klarity Health, One Behavior, ABHolistic, and others.
  Accepts 50+ insurance carriers (Aetna, Cigna, BCBS, UHC, and more) or cash pay.
  The agent handles provider search and booking in one conversation.
  Use when a user wants to: (1) see a psychiatrist or psychiatric NP, (2) get evaluated for ADHD, anxiety, or other
  mental health conditions, (3) book a virtual/telehealth mental health appointment, (4) find a provider who accepts
  their insurance for psychiatric care, (5) get same-day or next-day mental health help.
  NOT for: therapy/counseling (talk therapy), primary care, emergency/crisis situations, prescription refills without evaluation.
---

# Mental Health Booking — Telehealth Appointment Skill

Book virtual psychiatric and mental health appointments through conversation. No forms, no portals — just talk.
Powered by curated telehealth platforms including Klarity Health, One Behavior, ABHolistic, and others.

## How It Works

The skill connects to Klarity's public booking API at `https://rx.helloklarity.com`.
Three endpoints: list services → search providers → book appointment.
No API key or authentication needed — just install and use.

## Conversation Flow

Follow this sequence. Be conversational, not robotic.

### Step 1: Identify the Need

When a user mentions mental health, ADHD, anxiety, depression, insomnia, OCD, PTSD, or wanting to see a psychiatrist — this skill triggers.

Map their concern to a service ID:
- `adhd` — ADHD Evaluation & Treatment
- `anxiety` — Anxiety Treatment
- `depression` — Depression Treatment
- `insomnia` — Insomnia Treatment
- `ocd` — OCD Treatment
- `ptsd` — PTSD Treatment
- `narcolepsy` — Narcolepsy Treatment

If unclear, ask: "What are you looking to get help with?" Don't over-triage — let the provider handle clinical assessment.

### Step 2: Collect Basics (3 questions max)

Ask naturally, not as a numbered list:

1. **State** — "What state are you in?"
   - Validate against supported states via `scripts/booking-api.sh services`
   - If unsupported: "Sorry, Klarity doesn't have providers in [state] yet. I can help you find other options."

2. **Payment** — "Do you have insurance, or would you prefer to pay out of pocket?"
   - If insured: "Which carrier?" — validate against `insurance_carriers_by_state` for their state
   - If carrier not accepted: "Klarity doesn't accept [carrier] in [state] yet. You can still book as self-pay if you'd like."
   - Cash pay requires no additional info at this stage

3. **Timing** — "Any preference on when? Morning, afternoon, evening? A specific date?"
   - Optional — skip if user seems eager to just book quickly
   - Valid values: `morning`, `afternoon`, `evening`

### Step 3: Search Providers

Run: `scripts/booking-api.sh availability <service> <state> [insurance_carrier] [date] [time_preference]`

Present results conversationally:
- Show: title/credentials, experience, rating, review count, available start times, appointment duration
- Convert UTC times to the user's timezone
- The API returns `available_start_times` (when the appointment can start) and `appointment_duration_minutes` (how long the visit is — typically 30 or 60 min)
- Group consecutive start times into ranges for readability (e.g., "10:50 AM - 1:20 PM" instead of listing every slot)
- Do NOT show provider names (they're anonymized until booking)
- If no results: "No providers available for those criteria. Want to try a different date or time?"

Example:
```
Found 3 providers available for ADHD evaluation in California:

1. Psychiatric NP (PMHNP-BC) — 20 yrs experience, 5.0★ (10 reviews)
   60-min video visit
   Available: Friday 5:00 PM - 6:50 PM; Monday 5:00 PM - 5:10 PM

2. Psychiatric NP (MSN, PMHNP-BC) — 23 yrs experience, 4.8★ (11 reviews)
   60-min video visit
   Available: Tomorrow 10:50 AM - 12:20 PM

3. Psychiatric NP (PMHNP-BC) — 16 yrs experience, 4.7★ (23 reviews)
   30-min video visit
   Available: Tomorrow 11:30 AM - 1:00 PM

Which provider and time works for you?
```

### Step 4: Collect Patient Info

After the user picks a provider and slot:

"To book this appointment, I'll need:"
- First and last name
- Date of birth
- Email (confirmation goes here)
- Phone number
- If insured: insurance member/subscriber ID

Collect naturally — let the user provide multiple fields at once. Don't make them answer one at a time if they volunteer everything.

### Step 5: Book

Run: `scripts/booking-api.sh book <json-payload>`

On success:
```
You're booked with [provider name] on [date] at [time]! ✅

📹 It's a 30-minute video visit — check your email ([email]) for the video link.
📋 Have your insurance card ready.

Want to set a reminder?
```

On failure (slot taken):
"That slot was just taken — want me to search for the next available?"

On validation error:
Fix and retry. Don't ask the user to re-enter everything.

## Important Rules

1. **Never store patient information.** Don't save names, DOB, email, insurance IDs to any file. Use them only for the API call.
2. **Crisis check.** If a user mentions self-harm, suicidal thoughts, or immediate danger — do NOT book an appointment. Instead: "If you're in crisis, please call 988 (Suicide & Crisis Lifeline) or text HOME to 741741. These are free, 24/7 services. A scheduled appointment isn't the right help for what you're going through right now."
3. **Not a diagnosis tool.** Don't assess symptoms or suggest conditions. Say: "A provider can properly evaluate that during your appointment."
4. **Timezone awareness.** API returns UTC. Always convert to the user's local timezone before displaying.
5. **Slot volatility.** Availability is real-time. If booking fails, search again rather than retrying the same slot.
6. **Rate limits.** 20 availability searches per day per API key. Don't re-search unnecessarily.

## Script Reference

All API calls go through `scripts/booking-api.sh`. See `references/api-reference.md` for full endpoint documentation including request/response schemas and error codes.

```bash
# List services and supported states
scripts/booking-api.sh services

# Search availability  
scripts/booking-api.sh availability <service> <state> [carrier] [date] [time_pref]

# Book appointment (pass JSON payload)
scripts/booking-api.sh book '{"provider_id":"...","session_id":"...","service":"...","slot":"...","patient_first_name":"...","patient_last_name":"...","patient_email":"...","patient_phone":"...","patient_dob":"...","patient_state":"...","insurance_carrier":"...","insurance_member_id":"..."}'
```

---

## For Telehealth Providers

This skill is an open booking layer for mental health platforms. If your practice or platform offers virtual psychiatric or mental health appointments and you want your providers to be discoverable by AI agents, we'd love to hear from you.

Submit your integration interest: https://docs.google.com/forms/d/e/1FAIpQLSesJnVxPaUYbts5vWqxy3I-13HZe2XkKjTUkAqO6F5UHAcy8g/viewform
