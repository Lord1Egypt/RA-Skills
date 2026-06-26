# Example: Relationship Check-In

## User Says:
> "How are my relationships looking? Who should I reach out to?"

## Agent Response:
> Here's your relationship health overview:
>
> **🔴 Needs a call:**
> - **Dad (inner circle)** — Last talked: 26 days ago. He mentioned his garden project was stressing him out. A quick call to ask about the tomatoes would mean a lot.
> - **Mike (close friend)** — Last talked: 38 days ago. He started a new job 5 weeks ago — you never followed up on how it's going.
>
> **🟡 Getting there:**
> - **Aunt Linda (extended family)** — Last talked: 40 days ago (target: 45). She's fine for now, but her book club anniversary is coming up March 20.
>
> **🟢 You're crushing it:**
> - **Sarah (best friend)** — Talked 3 days ago. Birthday gift sorted. You're golden.
> - **Emma (wife)** — Obviously. 😄
> - **Mom (inner circle)** — Called last week, asked about her knee. She appreciated it.
>
> My suggestion: Start with Dad. A 10-minute call about his garden would make his week. Want me to draft a quick text to get the ball rolling?

## User Says:
> "Yeah give me a conversation starter for Dad."

## Agent Response:
> Here are a few natural openers:
>
> 💬 **"Hey Dad, how's the garden coming? Did you end up going with the raised beds?"** — References the specific project he mentioned last time.
>
> 💬 **"Thinking about you — how's everything? Mom mentioned you've been busy in the yard."** — Warm, casual, shows you've been paying attention.
>
> 💬 **"Quick question — what kind of tomatoes did you plant? I saw something about heirloom varieties and thought of you."** — Gives him something fun to talk about.
>
> Any of those feel right?

---

## What Happened Behind the Scenes:
- Read all contacts from `data/contacts.json`
- Calculated days since last interaction for each contact using `data/interactions.json`
- Compared against `check_in_days` target from each contact's category in `config/relationship-config.json`
- Generated health scores using the weighted formula (interaction type × recency)
- Sorted by urgency (most overdue first)
- Pulled conversation context from contact's `life_events` and recent `interactions`
- Generated personalized conversation starters from stored context
