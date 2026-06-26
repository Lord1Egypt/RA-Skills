# Home Maintenance OS

A conversational OpenClaw skill that tracks everything about your home: appliances, service history, contractors, and maintenance schedules. Supports multiple properties.

## What It Does

Tell it about your home in plain language and it builds a living record over time:

- **Appliances & Systems** -- make/model, install dates, warranties, notes
- **Service History** -- every repair, inspection, and maintenance visit with dates, costs, and who did the work
- **Contractor Directory** -- names, specialties, contact info, and quality notes (auto-populated from service logs)
- **Maintenance Reminders** -- recurring tasks with due dates calculated from your service history

## Example Usage

**Logging a service:**
> "The AC got serviced today by Blue Sky HVAC. Replaced the capacitor, $180."

**Checking history:**
> "When was the furnace last serviced?"

**Maintenance check:**
> "What's due for maintenance this month?"

**Contractor lookup:**
> "Who's our plumber?"

## Multi-Property Support

Tracks multiple homes (primary, rental, new purchase, etc.). Property context is maintained automatically once set. If you only have one property on file, it skips the property tags for cleaner output.

## Installation

Copy the `home-maintenance-os` folder into your OpenClaw skills directory and restart your agent.
