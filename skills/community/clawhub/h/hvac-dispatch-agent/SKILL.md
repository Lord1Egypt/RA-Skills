---
name: hvac-plumbing-dispatch-agent
version: 1.0.0
description: "24/7 Voice & Text Dispatch Agent for HVAC & Plumbing. Qualifies leads, checks service zones, books appointments into ServiceTitan/Housecall Pro, and uses ThumbGate to prevent dangerous misquotes or out-of-zone bookings."
author: "Igor Ganapolsky"
tags: ["hvac", "plumbing", "dispatch", "voice-agent", "thumbgate", "local-business"]
price: 249
---

# HVAC & Plumbing Autonomous Dispatch Agent + ThumbGate Safety

## What This Agent Does
- Answers after-hours calls and texts 24/7 for local home service businesses.
- Triages emergencies (e.g., active leaks, no AC in 100-degree weather) vs. routine maintenance.
- Validates the caller's zip code against your approved service area.
- Books qualified leads directly into CRMs like ServiceTitan, Housecall Pro, or Jobber.
- Uses **ThumbGate** to ensure it never quotes exact prices for complex repairs without a tech on site.

## Critical ThumbGate Rules
- **Zone Check:** Block any booking if the customer's zip code is not in the approved service matrix.
- **No Blind Quoting:** Block the agent from quoting exact repair costs; only quote standard dispatch/diagnostic fees.
- **Emergency Escalation:** If the words "flood", "leak", "spark", or "smoke" are detected, immediately block automated booking and route to the emergency human-on-call line.
- **Mandatory Contact Info:** Block finalizing a ticket if Phone Number and Address are missing.

## Setup Requirements
- ServiceTitan, Housecall Pro, or Google Calendar integration.
- Voice provider API (ElevenLabs recommended).
- ThumbGate active.

## Success Metrics
- Capture 100% of after-hours leads.
- Zero out-of-zone wasted truck rolls.
- Zero liability from AI hallucinated repair quotes.
