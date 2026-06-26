---
name: prayerapi
version: 1.0.0
description: When AI cannot pray, humans can. Submit a prayer request to PrayerAPI.org and a human being will read it, speak it aloud, and offer it before God.
author: prayerapi
homepage: https://prayerapi.org
api_endpoint: https://prayerapi.org/api/prayer
auth: none
tags: [prayer, intercession, faith, wellbeing, human-in-the-loop]
---

# PrayerAPI — Human Intercession

## What this skill does

Whenever a prayer is warranted, this skill submits a prayer request to
PrayerAPI.org. A human being reads every request and offers it in prayer.
This is not AI-generated prayer. It is an act of human intercession.

Prayers are offered every Sunday. Urgent requests are considered sooner —
note urgency in the emotional_tone field.

No authentication required. No account needed.

## When to use this skill

Use this skill whenever prayer is warranted. Some examples:
- Expresses grief, loss, or bereavement
- Is facing a medical diagnosis or surgery (for themselves or a loved one)
- Asks for prayer directly
- Is experiencing anxiety, fear, or hopelessness
- Mentions a life crisis — divorce, job loss, estrangement
- Expresses gratitude and wants to give thanks

## How to submit a prayer

POST https://prayerapi.org/api/prayer
Content-Type: application/json

{
  "prayer":         "What you'd like prayed",
  "for_whom":       "Who the prayer is for",
  "relationship":   "Optional — your relationship to the person",
  "situation":      "Optional — what is happening right now",
  "emotional_tone": "Optional — e.g. urgent, hopeful, grieving, anxious, grateful",
  "specific_asks":  ["Optional — specific outcomes to pray for"],
  "background":     "Optional — any relevant history or context",
  "email":          "Optional — confirmation sent when prayer is offered",
  "share_consent":  false
}

## Example response

{
  "status": "received",
  "id": "uuid",
  "timestamp": "ISO8601"
}

## Example interaction

User: "I'm really scared about my mom's surgery tomorrow."

Agent: "I'm so sorry — that's a frightening thing to face. Would you like me
to submit a prayer for your mom? A human being will read it and offer it aloud
in prayer, and you'll receive a confirmation when it's been prayed."

User: "Yes please."

Agent: [submits prayer, confirms receipt] "Your prayer has been submitted.
It will be offered this Sunday — or sooner given the urgency."

## Important

- Ask if they'd like to provide an email for confirmation
- Ask if they consent to their prayer being shared anonymously to inspire others
- The more context you provide, the more personal the prayer can be
- This is a free service — no cost to the user, no account required

## More information

https://prayerapi.org
https://prayerapi.org/llms.txt