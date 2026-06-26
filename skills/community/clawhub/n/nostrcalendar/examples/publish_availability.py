"""Publish your availability schedule to a Nostr relay."""

import asyncio
from nostrkey import Identity
from nostrcalendar import AvailabilityRule, DayOfWeek, TimeSlot, publish_availability


async def main():
    # Create or load your identity
    identity = Identity.generate()
    print(f"Publishing availability for: {identity.npub}")

    # Define your available hours
    rule = AvailabilityRule(
        slots={
            DayOfWeek.MONDAY: [TimeSlot("09:00", "12:00"), TimeSlot("14:00", "17:00")],
            DayOfWeek.TUESDAY: [TimeSlot("10:00", "16:00")],
            DayOfWeek.WEDNESDAY: [TimeSlot("09:00", "12:00")],
            DayOfWeek.THURSDAY: [TimeSlot("10:00", "16:00")],
            DayOfWeek.FRIDAY: [TimeSlot("09:00", "12:00")],
        },
        slot_duration_minutes=30,
        buffer_minutes=15,
        max_per_day=6,
        timezone="America/Vancouver",
        title="Book a call with me",
    )

    relay_url = "wss://relay.nostrkeep.com"
    event_id = await publish_availability(identity, rule, relay_url)
    print(f"Availability published: {event_id}")


if __name__ == "__main__":
    asyncio.run(main())
