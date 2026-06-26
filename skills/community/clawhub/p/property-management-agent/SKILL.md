---
name: property-management-ticketing-agent
version: 1.0.0
description: "Autonomous tenant maintenance and ticketing agent. Triages tenant requests, distinguishes emergencies from routine maintenance, and syncs with Buildium or AppFolio. Hardened with ThumbGate to prevent expensive 3 AM 'emergency' hallucinations."
author: "Igor Ganapolsky"
tags: ["real-estate", "property-management", "ticketing", "maintenance", "thumbgate"]
price: 347
---

# Autonomous Property Management Ticketing Agent + ThumbGate Safety

## What This Agent Does
- Answers tenant maintenance requests 24/7 via Voice and Text.
- Triages requests: Instantly identifies life-safety emergencies (e.g., active flood, gas smell) vs. routine repairs (e.g., dripping faucet).
- Validates the tenant's lease ID and unit number before creating a ticket.
- Syncs directly into Buildium, AppFolio, or Google Sheets.
- Uses **ThumbGate** to ensure the AI NEVER promises a same-day repair for non-emergencies.

## Critical ThumbGate Rules
- **Emergency Filter:** If words like "fire", "flood", "gas", or "sparks" are missing, block any "Emergency" ticket categorization.
- **Repair Capping:** Block the agent from authorizing any repair quote > 00 without a human landlord's explicit signature in ThumbGate.
- **Duplicate Guard:** Block ticket creation if a request for the same unit/category was submitted in the last 24 hours.

## Setup
1. Link your tenant database (Google Sheets or CRM).
2. Configure your emergency on-call contact.
3. Load skill: `openclaw skill load property-management-agent`
