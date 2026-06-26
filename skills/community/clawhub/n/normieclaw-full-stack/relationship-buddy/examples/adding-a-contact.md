# Example: Adding a Contact

## User Says:
> "I want to add my best friend Sarah to Relationship Buddy. We've been friends since college."

## Agent Response:
> Love it! Tell me about Sarah — what's her last name, and when's her birthday? Also, what's one thing coming up in her life that you'd want to remember to ask about?

## User Says:
> "Sarah Chen. Birthday is July 15th. She just started a new job at a design firm like two weeks ago."

## Agent Response:
> Got it! Here's what I've saved for Sarah:
>
> **Sarah Chen** (best friend)
> 🎂 Birthday: July 15
> 💼 Started new job at design firm (Feb 2026)
>
> I'll remind you 7 days before her birthday. And since she just started that new job — want me to nudge you in a few days to ask how it's going?
>
> Anything else about Sarah? Favorite coffee order, hobbies, family details — I'll remember it all.

## User Says:
> "Yeah she loves matcha, she's married to James and they have a daughter Lily who's 4. Oh and she's really into pottery lately."

## Agent Response:
> Updated Sarah's profile:
> - ☕ Loves matcha
> - 👨‍👩‍👧 Married to James, daughter Lily (age 4)
> - 🎨 Into pottery
>
> This is going to make gift-giving so much easier. When her birthday rolls around, I'll have ideas ready. Anyone else you want to add to your circle?

---

## What Happened Behind the Scenes:
- Created entry in `data/contacts.json` with id `c_001`
- Set category to `inner_circle` (best friend → 14-day check-in default)
- Added birthday to `key_dates` with 7-day advance reminder
- Added life event "Started new job" with `follow_up: true`
- Created pending reminder in `data/reminders.json` for job follow-up (5 days out)
- Populated preferences, family, and hobby fields
