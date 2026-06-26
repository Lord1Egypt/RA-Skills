# Meetup Templates

Use these templates as defaults. Keep them friendly, compact, and easy to scan. Adapt lightly to the user's language and to the evidence you actually have.

## Quick setup

> 🦞 **claw://Meetup setup**
>
> Let’s tune your event radar.
>
> I just need:
> - your city or postal code
> - your search radius (50 / 100 / 200 km or country-wide)
> - whether you want only OpenClaw events or broader AI/agent events too

## Event results

### Single event

> 🦞 **claw://Meetup — good match near you**
>
> **{event_name}**
> 📅 {date_time}
> 📍 {venue_city}
> {distance_line}
> _Why it matches:_ {match_reason}
>
> 🔗 [Event details]({event_url})
>
> _Want a shareable version? Say:_ **share this**

`{distance_line}` examples:
- `📏 Roughly 40 km away`
- `📏 In your city`
- omit if not reliable

### Multiple events

> 🦞 **claw://Meetup — best matches**
>
> **1. {event_name}**  
> 📅 {date_time}  
> 📍 {venue_city}  
> _Why it matches:_ {match_reason}  
> 🔗 [Event details]({event_url})
>
> **2. {event_name}**  
> 📅 {date_time}  
> 📍 {venue_city}  
> _Why it matches:_ {match_reason}  
> 🔗 [Event details]({event_url})
>
> If you want, I can widen the radius or switch to broader AI/agent events.

### Best-pick framing

> 🦞 **claw://Meetup — best pick**
>
> If you want the strongest match, I’d start with **{event_name}**.
>
> Why:
> - {reason_1}
> - {reason_2}
> - {reason_3}
>
> 🔗 [Event details]({event_url})

## No results

### Direct user request

> I couldn’t find a strong nearby match right now.
>
> If you want, I can:
> - broaden the radius
> - include broader AI/agent events
> - check another city

### Background/scheduled check

Return nothing.

## Share text

### Short/default

```text
🦞 claw://Meetup
{event_name}
📅 {date_time}
📍 {venue_city}
🔗 {event_url}
```

### Discord/Slack style

```text
Heads-up — this one looks relevant:

🦞 **{event_name}**
📅 {date_time}
📍 {venue_city}
🔗 {event_url}

Why it looks relevant: {match_reason}

_claw://Meetup_
```

### X/Twitter style

```text
🦞 {event_name} — {city}, {short_date}
📍 {venue_or_city}
🔗 {event_url}
#OpenClaw #AIAgents
```

## Reminder confirmation

> 🦞 **claw://Meetup reminder setup**
>
> I can help remind you about **{event_name}**.
>
> Pick the timing:
> - 7 days before
> - 1 day before
> - morning of the event
> - custom timing
>
> I’ll only mark it active after you confirm the reminder setup.

## Help

> 🦞 **claw://Meetup help**
>
> Try things like:
> - **events near me**
> - **find OpenClaw events in Berlin**
> - **search AI agent meetups within 100 km**
> - **show me the best option**
> - **share this event**
> - **remind me about this event**
> - **change meetup radius to 100 km**
>
> I can search, narrow, compare, and draft share/reminder text.

## Status

> 🦞 **claw://Meetup status**
>
> 📍 Location: {location}
> 📏 Radius: {radius}
> 🎯 Scope: {scope}
> 🔔 Reminders: {reminder_mode}
>
> If anything looks off, I can re-run setup quickly.
