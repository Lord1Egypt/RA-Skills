# Example: Birthday Reminder + Gift Suggestion

## Context:
Sarah Chen's birthday is July 15. Today is July 8 (7 days before). The agent proactively triggers a reminder.

## Agent Says (Proactive Nudge):
> 🎂 **Heads up — Sarah's birthday is next Tuesday!**
>
> Since she's been really into pottery and matcha lately, here are some gift ideas:
>
> 1. **Ceremonial Matcha Kit** ($35-45) — Includes stone-ground matcha, bamboo whisk, and ceramic bowl. She mentioned her whisk was cheap — this would be a perfect upgrade.
> 2. **Pottery Tool Set** ($25-40) — A quality set of sculpting and trimming tools for her new hobby.
> 3. **Handmade Ceramic Mug from Etsy** ($30-50) — You noted she mentioned wanting a nice ceramic mug. Support a small potter while you're at it.
>
> Last year you got her a pottery wheel starter kit and she loved it — so she's definitely into this stuff.
>
> Want me to look up specific products, or do you have something else in mind?

## User Says:
> "The matcha kit is perfect. She'd love that. Let me order it today."

## Agent Response:
> Great call! I'll log it so I don't suggest matcha stuff again for a while.
>
> Quick reminder — you'll want to get a card too. Sarah's address still the same? And want me to nudge you Tuesday morning to send her a birthday text?

## User Says:
> "Yeah same address. And yes, remind me Tuesday morning."

## Agent Response:
> Done! I've set:
> - 🎁 Gift logged: Ceremonial Matcha Kit for Sarah's birthday
> - 📱 Reminder: Tuesday 9 AM — text Sarah happy birthday
>
> She's going to love it.

---

## What Happened Behind the Scenes:
- Birthday reminder fired from `data/reminders.json` (7 days before)
- Gift suggestions pulled from contact preferences (matcha, pottery, ceramic mug mention)
- Gift history checked in `data/gifts.json` — pottery wheel kit given last Christmas, so avoided suggesting pottery wheel again
- New gift logged to `data/gifts.json`
- New reminder created for birthday morning text
- Reminder status updated to `completed`
