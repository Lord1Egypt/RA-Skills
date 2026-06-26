"""Request a human sponsor to co-sign events via NIP-46 bunker."""

import asyncio
from nostrkey import Identity
from nostrkey.bunker import BunkerClient


async def main():
    # Bot creates its own identity
    bot = Identity.generate()
    print(f"Bot npub: {bot.npub}")

    # Connect to a human's bunker (the human approves each signature)
    # Replace with a real bunker URI from NostrKey or another NIP-46 signer
    bunker_uri = "bunker://npub1human...?relay=wss://relay.damus.io"

    bunker = BunkerClient(bot.private_key_hex)
    await bunker.connect(bunker_uri)
    print("Connected to human sponsor's bunker")

    # The human sees a signing request and approves or denies
    signed = await bunker.sign_event(
        kind=1,
        content="This message was co-signed by my human sponsor",
    )
    print(f"Event signed: {signed.id}")


if __name__ == "__main__":
    asyncio.run(main())
