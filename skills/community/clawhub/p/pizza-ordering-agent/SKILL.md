---
name: ai-voice-pizza-ordering-agent
version: 1.0.0
description: "High-performance voice & text ordering agent for pizza shops. Specializes in complex customizations (half-and-half, crust types) and delivery zone validation. Hardened with ThumbGate to eliminate common pizza-specific mistakes."
author: "Igor Ganapolsky (ex-Subway Mobile App Team Lead)"
tags: ["pizza", "restaurant", "voice-agent", "ordering", "thumbgate", "mac-mini"]
price: 147
---

# AI Voice/Phone Pizza Ordering Agent with ThumbGate Safety

## What This Agent Does
- Handles complex pizza orders (custom toppings, half-and-half, crust preferences).
- Validates delivery addresses against a defined radius/zone.
- Upsells sides, drinks, and desserts based on order contents.
- Integrates with Google Sheets for Menu and Order Logging.
- Uses ThumbGate to prevent expensive topping or zone errors.

## Critical ThumbGate Rules
- **Zone Check:** Block any order where the address is outside the allowed delivery radius.
- **Customization Match:** Block orders with mutually exclusive toppings (e.g., vegan crust with non-vegan cheese) without confirmation.
- **Half-and-Half Logic:** Block any half-and-half order that doesn't explicitly confirm the base sauce for both sides.
- **Mandatory Phone Log:** Never finalize an order without capturing a valid callback number.

## Setup
1. Define your menu in Google Sheets.
2. Set your delivery radius in the ThumbGate config.
3. Load skill: `openclaw skill load pizza-ordering-agent`
