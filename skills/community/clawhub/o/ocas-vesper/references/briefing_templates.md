# Vesper Briefing Templates

## Output format

Plain text or minimal HTML for Gmail rendering. No markdown syntax. Bold via `<b>` only. Links as inline anchor text on the relevant words, never trailing labels.

## Morning briefing

```
Good morning Jared

58°F right now, ☁️ overcast, clearing to 63°F by 10am, ☀️ sunny.
High of 74°F mid-afternoon, ☀️ sunny, 71°F at 4pm, 🌤 partly cloudy, dropping to a low of 55°F overnight.

Saturday looks like 🌧 rain, Sunday ☀️ clearing mid-60s.

▪ Today
Coffee with Marcus at 10am (Blue Bottle, Mint Plaza)
Dermatology at 2:30pm (allow 15 min for parking)
Dinner reservation at 7pm, Nari (party of 4, confirmation #4821)

✉ Messages
David Chen replied to the Oahu thread, wants to confirm dates by Friday.
Two unread from your accountant, both re: Q1 estimated payments.

⚑ Logistics
Dry cleaning ready for pickup at Mulberry.
Japan visa application status still showing "in review."

◈ Markets
Portfolio closed yesterday at $142,830 (+0.3%). NVDA moved +2.1% on earnings guidance.

⟡ Decisions
The annual Bluesky domain renewal is due May 1 ($14). I can auto-renew or let it lapse if you want to reconsider.
```

In the rendered HTML version, these words become links:
- "10am", "2:30pm", "7pm" → Google Calendar event URIs
- "Blue Bottle, Mint Plaza", "Dermatology", "Nari" → Google Maps URIs
- "Oahu thread", "your accountant" → Gmail thread URIs
- "Mulberry" → Google Maps URI
- "in review" → visa status page URI

## Evening briefing

```
Good evening Jared

▪ Tomorrow
Team standup at 9am (Zoom)
Lunch with Sarah at noon (Tartine, Guerrero)

✉ Messages
Marcus confirmed coffee for tomorrow. No reply needed.
Your accountant is still waiting on the Q1 question.

◈ Markets
Portfolio opened at $142,830 and closed at $143,544 (+0.5%). No notable movers.

⟡ Decisions
The contractor needs a go/no-go on the bathroom tile by Wednesday. Two options in the shared doc, estimate difference is $400.
```

## Weather rules

Greeting line: "Good morning Jared" or "Good evening Jared". No punctuation after the greeting.

Weather appears only in morning briefings, immediately after the greeting.

Narrative format. Emoji always directly precedes the condition word it represents.

Required data points: current temp and condition, 10am forecast, high, 4pm forecast, low.

Friday only: append a weekend forecast line as a separate sentence.

No location callout when the owner is at home. When traveling, add context: "Here's what Tokyo looks like today." followed by the forecast narrative.

Evening briefings have no weather section.

## Weather emoji mapping

☀️ sunny/clear, 🌤 partly cloudy, ⛅ mostly cloudy, ☁️ overcast, 🌧 rain, 🌦 showers, ⛈ thunderstorms, 🌨 snow, 🌫 fog/haze, 💨 windy (use as modifier with another emoji)

## Section rules

Sections with no content are omitted entirely. No empty sections, no "nothing to report."

System section (⚙ System) only appears when something needs attention. Normal operation is silence.

Markets morning format: "Portfolio closed yesterday at $XXX,XXX (±X.X%)"
Markets evening format: "Portfolio opened at $XXX,XXX and closed at $XXX,XXX (±X.X%)"
Notable movers only when movement is material enough to mention.

Decisions: option, benefit, cost. Framed as optional. No pressure language.

## Opportunities

Surface the opportunity in natural language. Never expose the analysis. Example: "There's an opening at Gloss Nail Spa at 4:00 PM next Wednesday and that time is free on your calendar. Would you like me to book it?"

## Link rules

Every linkable item becomes an inline link. The words themselves are the anchor text.

URI patterns:
- Calendar events: `https://calendar.google.com/calendar/event?eid={event_id}`
- Locations: `https://maps.google.com/?q={place+name+address}`
- Gmail threads: `https://mail.google.com/mail/u/0/#inbox/{thread_id}`
- Tracking/status: direct link to carrier or service portal

If no ID is available to construct the link, skip the link rather than linking to a generic page.
