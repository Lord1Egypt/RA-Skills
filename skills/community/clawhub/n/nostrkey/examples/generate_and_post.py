"""Generate a Nostr identity and publish a text note to a relay."""

import asyncio
from nostrkey import Identity
from nostrkey.relay import RelayClient


async def main():
    # Create a fresh identity
    bot = Identity.generate()
    print(f"npub: {bot.npub}")

    # Introduce yourself (kind 0 = profile metadata)
    profile = bot.sign_event(
        kind=0,
        content='{"name":"my-openclaw-bot","about":"An AI agent with its own Nostr identity"}',
        tags=[],
    )

    # Post a text note (kind 1)
    note = bot.sign_event(
        kind=1,
        content="Hello from an OpenClaw bot!",
        tags=[["t", "openclaw"]],
    )

    # Publish both events
    async with RelayClient("wss://relay.damus.io") as relay:
        await relay.publish(profile)
        await relay.publish(note)
        print(f"Published profile and note as {bot.npub}")

    # Save identity for next time (encrypted at rest)
    bot.save("my-bot.nostrkey", passphrase="change-me")
    print("Identity saved to my-bot.nostrkey")


if __name__ == "__main__":
    asyncio.run(main())
