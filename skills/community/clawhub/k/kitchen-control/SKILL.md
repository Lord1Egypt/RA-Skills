# Freezer Inventory Management Skill for OpenClaw

## Overview

This skill manages freezer inventory in a convenience store via WhatsApp commands. It tracks inventory with expiration dates, logs sales, creates schedules for display, dynamically adjusts pricing based on cost and expiration, and uses an AI API for forecasting demand.

## Features

- Parse WhatsApp text commands: inventory input, sales updates, schedule requests
- Integrate with PocketBase for persistent storage
- Apply cost-aware dynamic pricing discounts
- Call external AI API for sales forecasting and price recommendations
- Provide WhatsApp-formatted response messages
- Basic user role-based authorization

## Usage

Deploy in OpenClaw runtime with environment variables configured for PocketBase and AI API.
Connect your WhatsApp webhook to route messages to this skill.

## Files

- freezer_inventory_skill.js — main skill code

---

## Installation

1. Place the skill directory `freezer_inventory_skill/` inside your OpenClaw skills folder.
2. Configure environment variables:
   - `POCKETBASE_URL`, `POCKETBASE_ADMIN_TOKEN` for PocketBase access
   - `AI_API_KEY`, `AI_API_URL` for forecasting API
3. Register and enable the skill in your OpenClaw instance.
4. Route WhatsApp webhook messages to this skill.

## Commands

- `inventory item1 qty1 item2 qty2 expiration YYYY-MM-DD`
- `sold item qty`
- `schedule`

## Notes

- Extend integration with real WhatsApp API for message sending.
- User authentication mapped by WhatsApp number.
- Logging enabled for debugging.
