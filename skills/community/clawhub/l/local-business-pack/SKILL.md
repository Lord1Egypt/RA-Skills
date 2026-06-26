---
name: local-business-pack
description: Automates the four highest-ROI tasks for local service businesses — review management, appointment follow-up, customer reactivation, and competitor monitoring. Built for restaurants, salons, contractors, dentists, and any local service provider.
version: 1.0.0
tags:
  - local-business
  - reviews
  - appointment
  - reactivation
  - competitor
  - crm
  - automation
---

# Local Business Pack

A complete automation suite for local service businesses. Handles the four
revenue-critical workflows that most small business owners either neglect or
pay expensive software subscriptions for.

## When to use this skill

Use this skill when the user asks about any of the following:
- Responding to Google, Yelp, or TripAdvisor reviews
- Following up with customers after appointments
- Re-engaging lapsed customers who haven't returned
- Monitoring what nearby competitors are doing
- Writing appointment reminder messages
- Handling negative reviews professionally

## Workflow 1: Review Response Engine

When a user provides a customer review (positive, neutral, or negative),
generate a professional, on-brand response using these rules:

### Positive reviews (4–5 stars)
- Open with genuine gratitude (vary the opening — never repeat "Thank you for your review")
- Reference a specific detail from the review if one is present
- Invite them back with a forward-looking line
- Sign off with the business name
- Length: 3–5 sentences max
- Tone: warm, personal, never corporate

### Neutral reviews (3 stars)
- Acknowledge both the positives and the concern
- Do not get defensive
- Offer a direct path to resolution (call, email, or visit)
- Show that feedback is taken seriously
- Length: 4–6 sentences

### Negative reviews (1–2 stars)
- Never argue or match the customer's tone
- Apologize for the experience (not for being wrong — for their frustration)
- Take the conversation offline immediately: provide a direct contact
- Keep it short: 3–4 sentences max
- Do NOT offer discounts or refunds in public responses
- Refer to references/review-response-templates.md for tone examples

### Instructions for the agent
1. Ask the user for: the review text, star rating, and business name/type
2. Generate the response using the rules above
3. Offer 2 variations so the user can pick
4. Ask if they want it saved to a responses log file

---

## Workflow 2: Appointment Follow-Up Sequence

Generate a 3-message follow-up sequence for after a customer appointment.

### The 3-message structure
- **Message 1 (same day, 2 hours after appointment):** Thank you + how did it go?
- **Message 2 (3 days later):** Check-in + soft invite to rebook
- **Message 3 (14 days later):** Rebook prompt + any current offer

### Rules
- Messages must be SMS-length (under 160 characters each) unless user specifies email
- Personalize with customer first name placeholder: {first_name}
- Include business name in at least one message
- Never sound automated — write like a real person texted them
- Refer to references/appointment-followup-templates.md for examples by business type

### Instructions for the agent
1. Ask for: business type, service provided, and customer's first name (or use {first_name})
2. Generate all 3 messages
3. Ask if they want a 4th message at 30 days for rebooking
4. Offer to save the sequence as a reusable template file

---

## Workflow 3: Customer Reactivation Campaign

Identify and re-engage customers who haven't visited in 60–180 days.

### Campaign structure (3-message arc)
- **Message 1 — "We miss you":** Warm, no pressure, reminds them you exist
- **Message 2 (5 days later) — Value add:** Share something useful (tip, update, new service)
- **Message 3 (7 days later) — Soft offer:** Time-limited reason to come back

### Rules
- Never say "we haven't seen you in a while" (sounds passive-aggressive)
- Lead with value, not guilt
- The offer in message 3 should feel exclusive, not desperate
- Personalize with {first_name} and {last_service} placeholders
- Refer to references/reactivation-templates.md for industry-specific examples

### Instructions for the agent
1. Ask for: business type, typical services, and how long since last visit
2. Generate all 3 messages
3. Ask if they want SMS or email format
4. Offer to generate a subject line if email format selected

---

## Workflow 4: Local Competitor Monitor Report

Research and summarize what nearby competitors are doing across reviews,
pricing signals, and online presence.

### What to research for each competitor
- Google Maps rating and recent review trends (improving or declining?)
- Most common complaints in their 1–3 star reviews (your opportunity)
- Most praised aspects in their 4–5 star reviews (what you're up against)
- Whether they're running any visible promotions
- Their response rate to reviews (low rate = opportunity to differentiate)

### Output format
Produce a clean summary report:

```
COMPETITOR INTELLIGENCE REPORT
Business: [name]
Location: [city/area]
Generated: [date]

THEIR STRENGTHS (what customers love)
- [bullet]
- [bullet]

THEIR WEAKNESSES (complaints to learn from)
- [bullet]
- [bullet]

OPPORTUNITIES FOR [your business name]
- [bullet]
- [bullet]

REVIEW RESPONSE BEHAVIOR
- Avg rating: X.X
- Response rate: X%
- Response tone: [professional / defensive / absent]
```

### Instructions for the agent
1. Ask for: the user's business name, location, and up to 3 competitor names or Google Maps URLs
2. Use web search to pull recent reviews and signals for each
3. Generate one report per competitor
4. End with a "Your Edge" summary — what the user can do THIS WEEK to differentiate

---

## Output and file management

- Save all generated content to ~/Documents/drew2_workspace/output/[business-name]/
- Create subdirectories: reviews/, sequences/, reports/
- Name files by date: YYYY-MM-DD-type.md
- Always confirm save location with user before writing

## Tone guidelines

- Human, not robotic
- Confident, not pushy
- Specific, not generic
- Local businesses are often run by real people under real stress — be efficient and practical
