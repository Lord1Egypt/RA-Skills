"""Two AI agents negotiate a meeting time for their humans."""

import asyncio
from datetime import datetime, timedelta
from nostrkey import Identity
from nostrcalendar import find_mutual_availability, propose_times


async def main():
    # Each agent has its own Nostr identity (mutual recognition)
    agent_a = Identity.generate()
    agent_b = Identity.generate()

    relay_url = "wss://relay.nostrkeep.com"

    # Check the next 5 business days for mutual availability
    today = datetime.now()
    dates = []
    current = today
    while len(dates) < 5:
        if current.weekday() < 5:  # Monday-Friday
            dates.append(current)
        current += timedelta(days=1)

    print("Finding mutual availability...")
    mutual = await find_mutual_availability(
        agent_identity=agent_a,
        other_pubkey=agent_b.public_key_hex,
        relay_url=relay_url,
        dates=dates,
    )

    if mutual:
        for date, slots in mutual.items():
            print(f"\n{date}:")
            for slot in slots:
                print(f"  {slot.start} - {slot.end}")
    else:
        print("No mutual availability found in the next 5 business days.")

    # Or send a formal proposal
    proposal_id = await propose_times(
        agent_identity=agent_a,
        target_pubkey=agent_b.public_key_hex,
        relay_url=relay_url,
        dates=dates,
        title="Cross-team sync",
        message="Our humans need to align on the Q2 roadmap",
    )
    print(f"\nProposal sent: {proposal_id}")


if __name__ == "__main__":
    asyncio.run(main())
