"""Publish a Nostr profile for your AI agent."""

import asyncio
import os

from nostrkey import Identity
from nostr_profile import Profile, publish_profile, get_profile, update_profile


async def main():
    identity = Identity.from_nsec(os.environ["NOSTR_NSEC"])
    relay = os.environ.get("NOSTR_RELAY", "wss://relay.nostrkeep.com")

    # Create and publish a profile
    profile = Profile(
        name="Johnny5",
        about="An OpenClaw AI companion",
        picture="https://example.com/johnny5-avatar.png",
        nip05="johnny5@example.com",
        website="https://example.com",
    )

    event_id = await publish_profile(identity, profile, relay)
    print(f"Profile published: {event_id}")

    # Read it back
    fetched = await get_profile(identity.public_key_hex, relay)
    if fetched:
        print(f"\nProfile on relay:")
        print(f"  Name: {fetched.name}")
        print(f"  About: {fetched.about}")
        print(f"  NIP-05: {fetched.nip05}")

    # Update just the about field
    event_id = await update_profile(identity, relay, about="Updated bio — now with scheduling!")
    print(f"\nProfile updated: {event_id}")


if __name__ == "__main__":
    asyncio.run(main())
