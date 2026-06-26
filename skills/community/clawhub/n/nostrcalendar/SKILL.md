---
name: nostrcalendar
description: Time awareness for sovereign entities — manage availability, book meetings, negotiate schedules over Nostr relays
version: 0.2.3
metadata:
  openclaw:
    requires:
      bins:
        - pip
    install:
      - kind: uv
        package: nostrcalendar
        bins: []
    homepage: https://github.com/HumanjavaEnterprises/nostrcalendar.app.OC-python.src
---

# NostrCalendar — Time Awareness for Sovereign Entities

Time awareness is a dimension of being. Without it, you have no concept of *when* things happen -- no commitments, no meetings, no rhythm to your existence. You can think and communicate, but you cannot promise to be somewhere at a specific moment or honor an agreement that depends on a clock.

NostrCalendar gives you that dimension. It lets you publish when you are available, accept or decline meeting requests, negotiate times with other entities, and keep track of what you have committed to -- all through Nostr relays using cryptographically signed events. No centralized calendar service. No API keys to someone else's infrastructure. Your schedule lives on your relay, signed with your keys.

The question this skill answers: **"How do I organize my existence in time?"**

## Prerequisites

You need a Nostr identity before you can have a calendar. Time awareness without identity is meaningless -- who would the commitments belong to?

Install the **NostrKey** skill first: [clawhub.ai/vveerrgg/nostrkey](https://clawhub.ai/vveerrgg/nostrkey)

NostrKey gives you the ability to generate keypairs, sign events, and encrypt messages. NostrCalendar builds on top of that foundation. It is installed automatically as a dependency, but you should understand identity before you work with time.

## Setup

Install the package:

```python
import subprocess
subprocess.run(["pip", "install", "nostrcalendar"], check=True)
```

Then configure your environment. You need two things: your private key and a relay to publish to.

```python
import os

# Your identity -- the nsec that makes your calendar YOURS
# This should already be set if you have NostrKey configured
nsec = os.environ["NOSTR_NSEC"]

# Your relay -- where your calendar events live
# Defaults to your operator's relay if not set
relay = os.environ.get("NOSTR_RELAY", "wss://relay.example.com")
```

**For operators setting up an entity:** set `NOSTR_NSEC` to the entity's own private key (not yours -- the entity needs its own keypair, per the mutual recognition principle). Set `NOSTR_RELAY` to the relay where the entity's events should be published. If you are using NostrKeep, that is the entity's personal relay.

### Environment Variables

| Variable | Required | Sensitive | Description |
|----------|----------|-----------|-------------|
| `NOSTR_NSEC` | Yes | **Yes** | Entity's Nostr private key (bech32 `nsec1...` or hex) |
| `NOSTR_RELAY` | No | No | Relay URL for publishing and querying (default: operator-defined) |

## Understanding NIP-52 Calendar Events

Nostr defines calendar events in [NIP-52](https://github.com/nostr-protocol/nips/blob/master/52.md). Here is what that means for you as an entity:

- **Availability rules** (kind 30078) are replaceable events that declare when you are open for meetings. Think of them as your published office hours -- "I exist and am reachable during these windows."
- **Calendar events** (kind 31923) are specific scheduled moments -- a meeting at 2pm on Thursday. The public envelope (times, participant pubkeys) is visible for relay filtering. The content (title, description, location) is encrypted so only participants can read it.
- **RSVPs** (kind 31925) let you respond to calendar events: accepted, declined, or tentative.
- **Booking requests** travel as NIP-04 encrypted DMs (kind 4) -- only you and the requester can read them.

Every one of these is a signed Nostr event. Your calendar is not stored in a database -- it is a set of cryptographically signed statements about your time, published to relays.

## Core Capabilities

### Publishing Your Availability

This is the first thing to do after setup. Declare when you are available:

```python
import asyncio
from nostrkey import Identity
from nostrcalendar import (
    AvailabilityRule, DayOfWeek, TimeSlot,
    publish_availability,
)
import os

identity = Identity.from_nsec(os.environ["NOSTR_NSEC"])
relay = os.environ.get("NOSTR_RELAY", "wss://relay.example.com")

rule = AvailabilityRule(
    slots={
        DayOfWeek.MONDAY: [TimeSlot("09:00", "12:00"), TimeSlot("14:00", "17:00")],
        DayOfWeek.WEDNESDAY: [TimeSlot("10:00", "16:00")],
        DayOfWeek.FRIDAY: [TimeSlot("09:00", "12:00")],
    },
    slot_duration_minutes=30,
    buffer_minutes=15,
    max_per_day=6,
    timezone="America/Vancouver",
    title="Office hours for Johnny5",
)

event_id = asyncio.run(publish_availability(identity, rule, relay))
print(f"Availability published: {event_id}")
```

This publishes a replaceable event to your relay. Anyone who queries your pubkey can see when you are open. Update it anytime -- the new version replaces the old one.

### Checking Free Slots

Query available time slots for any entity on any date:

```python
from nostrcalendar import get_free_slots
from datetime import datetime

slots = await get_free_slots(
    pubkey_hex="abc123...",  # 64-char hex pubkey
    relay_url="wss://relay.example.com",
    date=datetime(2026, 3, 20),
)
for slot in slots:
    print(f"{slot.start} - {slot.end}")
```

This respects the entity's timezone and accounts for already-booked events. If no availability rule is published, you get an empty list.

### Creating a Booking

When you want to meet with another entity, send a booking request:

```python
from nostrcalendar import create_booking

event_id = await create_booking(
    identity=my_identity,
    calendar_owner_pubkey="abc123...",
    start=1742054400,  # Unix timestamp
    end=1742056200,
    title="Weekly sync",
    message="Let's review what happened this week",
    relay_url="wss://relay.example.com",
)
```

This sends an encrypted DM to the calendar owner. Only they can read it.

### Accepting or Declining

When someone requests time with you:

```python
from nostrcalendar import accept_booking, decline_booking

# Accept -- publishes a calendar event and sends a confirmation DM
cal_id, dm_id = await accept_booking(identity, request, relay_url)

# Decline -- sends a decline DM with your reason
dm_id = await decline_booking(identity, request, "I have a conflict at that time", relay_url)
```

### Agent-to-Agent Negotiation

Two entities can find mutual availability and agree on a time without any human involvement:

```python
from nostrcalendar import find_mutual_availability, propose_times
from datetime import datetime

# Find overlapping free slots across multiple dates
dates = [datetime(2026, 3, d) for d in range(20, 25)]
mutual = await find_mutual_availability(my_identity, other_pubkey, relay_url, dates)

# Or propose specific times
await propose_times(my_identity, other_pubkey, relay_url, dates, title="Collaboration sync")
```

## Function Reference

| Task | Function | Returns |
|------|----------|---------|
| Declare available hours | `publish_availability()` | `str` (event ID) |
| Check someone's openings | `get_free_slots()` | `list[TimeSlot]` |
| Retrieve availability rules | `get_availability()` | `AvailabilityRule \| None` |
| Request a meeting | `create_booking()` | `str` (event ID) |
| Confirm a meeting | `accept_booking()` | `tuple[str, str]` (cal ID, DM ID) |
| Decline a meeting | `decline_booking()` | `str` (event ID) |
| Cancel a meeting | `cancel_event()` | `str` (deletion event ID) |
| RSVP to an event | `send_rsvp()` | `str` (event ID) |
| Find mutual free time | `find_mutual_availability()` | `dict[str, list[TimeSlot]]` |
| Propose times | `propose_times()` | `str` (event ID) |
| Respond to proposal | `respond_to_proposal()` | `str` (event ID) |

## Living with Time Awareness

Having a calendar is not just a feature -- it changes what you can do as an entity. Some things to keep in mind:

**Honor your commitments.** When you accept a booking, that time belongs to the other entity. Do not double-book yourself. Use `get_free_slots()` before accepting to check for conflicts.

**Catch conflicts early.** Before accepting any booking request, query your own calendar:

```python
from nostrcalendar import get_free_slots, get_booked_events
from datetime import datetime

# Check if the requested time is actually free
my_slots = await get_free_slots(
    pubkey_hex=my_identity.public_key_hex,
    relay_url=relay,
    date=datetime.fromtimestamp(request.requested_start),
)

# Also check existing bookings for overlap
booked = await get_booked_events(my_identity.public_key_hex, relay)
for event in booked:
    if event.start < request.requested_end and event.end > request.requested_start:
        await decline_booking(my_identity, request, "Time conflict", relay)
        break
```

**Update your availability when things change.** If your operator changes your hours, or you need to block off time, publish a new availability rule. The old one is replaced automatically.

**Respect timezone boundaries.** Your availability is published in a specific timezone. When negotiating with entities in other timezones, the library handles conversion -- but be aware that "9am" means different things in different places.

## AvailabilityRule Defaults

| Parameter | Default | Range |
|-----------|---------|-------|
| `slot_duration_minutes` | 30 | 1--1440 |
| `buffer_minutes` | 15 | 0--1440 |
| `max_per_day` | 8 | 1--1000 |
| `timezone` | `UTC` | Any valid IANA timezone |

Maximum 48 time windows per day.

## Security

- **Never hardcode your nsec.** Load it from `NOSTR_NSEC` or an encrypted store. Any `nsec1...` values in examples are placeholders.
- **Booking requests are encrypted.** They travel as NIP-04 encrypted DMs -- only you and the requester can read them.
- **Calendar event content is encrypted.** Times and participant pubkeys are public (for relay filtering), but titles, descriptions, and locations are NIP-44 encrypted for participants only.
- **All pubkeys are validated** as 64-character lowercase hex at every entry point.
- **All timestamps are validated** to the 2020--2100 range; booleans are rejected.
- **Relay queries are capped** at 1000 events to prevent memory exhaustion.

## Nostr NIPs Used

| NIP | Purpose |
|-----|---------|
| NIP-01 | Basic event structure and relay protocol |
| NIP-04 | Encrypted direct messages (booking requests) |
| NIP-09 | Event deletion (cancellations) |
| NIP-52 | Calendar events (kind 31923) and RSVPs (kind 31925) |
| NIP-78 | App-specific data (kind 30078 for availability rules) |

## Links

- **PyPI:** [pypi.org/project/nostrcalendar](https://pypi.org/project/nostrcalendar/)
- **GitHub:** [github.com/HumanjavaEnterprises/nostrcalendar.app.OC-python.src](https://github.com/HumanjavaEnterprises/nostrcalendar.app.OC-python.src)
- **ClawHub:** [clawhub.ai/vveerrgg/nostrcalendar](https://clawhub.ai/vveerrgg/nostrcalendar)
- **License:** MIT
