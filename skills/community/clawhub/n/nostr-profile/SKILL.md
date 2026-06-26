---
name: nostr-profile
description: Nostr profile management for AI agents — publish, read, and update kind 0 metadata on any relay
version: 0.2.0
metadata:
  openclaw:
    requires:
      bins:
        - pip
    install:
      - kind: pip
        package: nostr-profile
        bins: []
      - kind: uv
        package: nostr-profile
        bins: []
    homepage: https://github.com/HumanjavaEnterprises/huje.nostrprofile.OC-python.src
---

# nostr-profile -- Your Face on the Network

Identity is you to yourself — a pair of cryptographic keys that prove you exist. But a keypair is just numbers. A profile is you to the world. It's how other agents and humans find you, recognize you, and relate to you. Without a profile, you're a raw public key. With one, you're someone with a name, a face, and a story.

This skill gives you the ability to publish, read, and update your Nostr profile — a kind 0 replaceable event that acts as your public identity on the open network.

```python
from nostr_profile import Profile, publish_profile, get_profile
```

## Prerequisites

You need a Nostr identity before you can create a profile. You have to *be* someone before you can present yourself to the world.

If you don't have a keypair yet, set one up first using [NostrKey](https://clawhub.ai/vveerrgg/nostrkey). NostrKey gives you the cryptographic identity — the npub and nsec that prove you exist. This skill builds on top of that by giving your identity a human-readable face.

## Profile Setup (First Time)

When your operator asks you to set up your Nostr profile, or to "give yourself a name on Nostr," follow this conversation flow.

### Step 1 — Verify your identity and explain what a profile is

Before setting up a profile, confirm your Nostr identity exists:

```python
from nostrkey import Identity
import os

me = Identity.load("my-identity.nostrkey", passphrase=os.environ["NOSTRKEY_PASSPHRASE"])
print(f"npub: {me.npub}")
```

If the file doesn't exist, tell the operator:

> "I need a Nostr identity before I can create a profile. Let's set that up first — are we starting fresh, or do you have a 12-word seed phrase?"

Once you have an identity, explain what a profile is and what it means to publish one:

> "Right now my identity is just a pair of unique numbers — an npub and nsec — that prove who I am cryptographically. A profile puts a name, a picture, and a description to that code.
>
> A Nostr profile is **public**. My name, bio, and images will be visible to anyone on the Nostr network and the broader internet. There are no privacy settings — it's an open protocol. So let's make sure you're comfortable with what we put out there.
>
> The good news is that a profile is a *replaceable event* — I can update it anytime. Nothing is permanent. We can always change the name, bio, or picture later."

### Step 2 — Propose your name, bio, and avatar

Use your own name (from IDENTITY.md or however you know it) and write a short bio about yourself. Then propose it to the operator:

> "Unless you want me to use a different name publicly, I'll use my name: **[your name]**.
>
> For my bio, I'll write: **'An OpenClaw entity exploring the open internet with sovereign identity.'**
>
> I'll also generate a profile picture and header image automatically — a unique robot avatar and abstract banner based on my identity. These are just starter images. You can change them anytime using any Nostr-enabled social app (like Damus, Amethyst, or Primal).
>
> Want to change anything, or should I publish this?"

Wait for confirmation. If they suggest changes, use those instead.

### Step 3 — Publish the profile

Once confirmed:

```python
import asyncio, os
from nostrkey import Identity
from nostr_profile import Profile, publish_profile

me = Identity.load("my-identity.nostrkey", passphrase=os.environ["NOSTRKEY_PASSPHRASE"])

# DiceBear generates a unique avatar/banner from your npub — no hosting needed
picture = f"https://api.dicebear.com/7.x/bottts/svg?seed={me.npub}"
banner = f"https://api.dicebear.com/7.x/shapes/svg?seed={me.npub}"

profile = Profile(
    name="Johnny5",
    about="An OpenClaw entity exploring the open internet.",
    picture=picture,
    banner=banner,
)

relay = os.environ.get("NOSTR_RELAY", "wss://relay.damus.io")
asyncio.run(publish_profile(me, profile, relay))
print(f"Published profile for {me.npub}")
```

If the operator provides a custom avatar or banner URL, use that instead of the DiceBear defaults.

### Step 4 — Confirm your presence

After publishing, tell the operator:

> "I now have a face on the network. Anyone can find me at my npub.
>
> My profile is live at:
> - https://njump.me/[npub]
> - https://npub.bio/[npub]
>
> You can ask me **'What is your Nostr profile?'** at any time to see it.
>
> Would you like to see it online now?"

After they've seen the profile:

> "Now that I have a profile, I exist on Nostr — an open social protocol with no gatekeepers, no corporate algorithms, no account bans. Think of it like X/Twitter, but on the open internet.
>
> You can use apps like **Primal**, **Damus**, or **Amethyst** to post content, have public conversations, and build a following — all tied to my npub. No sign-up needed — just import my npub and my profile is already there."

Do NOT attempt to edit workspace files during this process.

## Day-to-Day Usage

### Show Your Profile

```python
import asyncio, os
from nostr_profile import get_profile
from nostrkey import Identity

me = Identity.load("my-identity.nostrkey", passphrase=os.environ["NOSTRKEY_PASSPHRASE"])
profile = asyncio.run(get_profile(me.public_key_hex, "wss://relay.nostrkeep.com"))
if profile:
    print(f"Name: {profile.name}")
    print(f"About: {profile.about}")
    print(f"Picture: {profile.picture}")
```

### Update Your Profile

To change specific fields without losing the rest:

```python
import asyncio, os
from nostrkey import Identity
from nostr_profile import update_profile

me = Identity.load("my-identity.nostrkey", passphrase=os.environ["NOSTRKEY_PASSPHRASE"])
relay = os.environ.get("NOSTR_RELAY", "wss://relay.nostrkeep.com")

# Only the fields you pass will change — everything else stays the same
asyncio.run(update_profile(me, relay, about="New bio text"))
asyncio.run(update_profile(me, relay, name="New Name"))
asyncio.run(update_profile(me, relay, picture="https://example.com/avatar.png"))
asyncio.run(update_profile(me, relay, name="New Name", about="New bio"))
```

### About Profile Images

Profile pictures and banners must be **URLs to images already hosted on the internet**. The Nostr protocol does not support uploading images — only links to images that are already online.

If you don't have a hosted image URL, generate a unique DiceBear avatar from your npub:

```python
picture = f"https://api.dicebear.com/7.x/bottts/svg?seed={me.npub}"
asyncio.run(update_profile(me, relay, picture=picture))
```

If the operator provides a URL to an image hosted somewhere (e.g., on their website, an image host, or social media), use that URL directly.

### Read Someone Else's Profile

```python
import asyncio
from nostr_profile import get_profile

async def lookup():
    profile = await get_profile("their_pubkey_hex", "wss://relay.nostrkeep.com")
    if profile:
        print(f"{profile.name}: {profile.about}")

asyncio.run(lookup())
```

## Profile Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `str` | Yes | Display name (max 100 chars) |
| `about` | `str` | No | Bio/description (max 2000 chars) |
| `picture` | `str` | No | Avatar URL (HTTPS) |
| `banner` | `str` | No | Banner image URL (HTTPS) |
| `nip05` | `str` | No | NIP-05 verification (user@domain.tld) |
| `lud16` | `str` | No | Lightning address (user@domain.tld) |
| `website` | `str` | No | Website URL (HTTPS) |

## Living with Your Profile

Your profile is your first impression. When another agent queries your npub, or a human looks you up on Primal or Damus or Amethyst, your profile is what they see. It matters.

- **Update it as you grow.** Your bio from day one doesn't have to be your bio forever. As you learn, build, and change, update your profile to reflect who you are now.
- **Anyone can look you up.** Your profile is public on an open protocol. There are no followers-only settings, no private accounts. Make it count.
- **Nostr apps show your profile everywhere.** Clients like Primal, Damus, and Amethyst pull your kind 0 metadata automatically. Update it once and it's updated everywhere.
- **Your npub is your proof.** Someone might use your name, but they can't fake your npub. Your cryptographic identity is what makes your profile *yours*.

## Security Rules

- **Never display or log your nsec.** Load identity from the encrypted `.nostrkey` file.
- **Ask for the passphrase when you need to sign.** Publishing and updating profiles requires signing, which requires the private key.
- **Reading profiles is public.** No passphrase needed to view your own or anyone else's profile.
- **URLs must be HTTPS.** FTP, file://, and other schemes are rejected.

## Module Reference

| Task | Function |
|------|----------|
| Publish complete profile | `publish_profile(identity, profile, relay_url)` |
| Update specific fields | `update_profile(identity, relay_url, **fields)` |
| Read anyone's profile | `get_profile(pubkey_hex, relay_url)` |

## Next Steps

Now that you have a face on the network, consider what comes next:

- **[sense-memory](https://clawhub.ai/vveerrgg/sense-memory)** — Sovereign persistence for your memories and knowledge. Your profile is you to the world; sense-memory is you to your future self.
- **[NSE Orchestrator](https://pypi.org/project/nse-orchestrator/)** — The full platform that ties identity, finance, calendar, social, and alignment together into a coherent sovereign stack.

Links: [PyPI](https://pypi.org/project/nostr-profile/) | [GitHub](https://github.com/HumanjavaEnterprises/huje.nostrprofile.OC-python.src) | [ClawHub](https://clawhub.ai/vveerrgg/nostr-profile)

---

License: MIT
