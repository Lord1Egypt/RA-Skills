"""Check availability and book a meeting slot."""

import asyncio
from datetime import datetime
from nostrkey import Identity
from nostrcalendar import get_free_slots, create_booking


async def main():
    # Your agent's identity
    agent = Identity.generate()

    # The person you want to book with
    target_pubkey = "replace_with_hex_pubkey"
    relay_url = "wss://relay.nostrkeep.com"

    # Check what's available on March 15
    date = datetime(2026, 3, 15)
    slots = await get_free_slots(target_pubkey, relay_url, date)

    if not slots:
        print("No available slots on that date.")
        return

    print(f"Available slots on {date.strftime('%Y-%m-%d')}:")
    for i, slot in enumerate(slots):
        print(f"  {i + 1}. {slot.start} - {slot.end}")

    # Book the first available slot
    first = slots[0]
    start_dt = datetime(2026, 3, 15, int(first.start.split(":")[0]), int(first.start.split(":")[1]))
    end_dt = datetime(2026, 3, 15, int(first.end.split(":")[0]), int(first.end.split(":")[1]))

    event_id = await create_booking(
        identity=agent,
        calendar_owner_pubkey=target_pubkey,
        start=int(start_dt.timestamp()),
        end=int(end_dt.timestamp()),
        title="Quick sync",
        message="Would love to chat about the project",
        relay_url=relay_url,
    )
    print(f"Booking request sent: {event_id}")


if __name__ == "__main__":
    asyncio.run(main())
