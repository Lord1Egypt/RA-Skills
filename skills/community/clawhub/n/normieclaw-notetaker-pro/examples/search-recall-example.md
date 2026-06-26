# Example: Search & Recall

## Scenario 1: Natural Language Recall

### User Input

> What was that sushi place Sarah mentioned?

### Agent Response

> 🔍 Found it:
>
> **Kura Sushi — Pearl Street**
> 📅 March 8, 2026 | #restaurant #recommendation #sarah
> Sushi restaurant recommended by Sarah. Located on Pearl Street.

---

## Scenario 2: Tag-Based Browse

### User Input

> Show me all my meeting notes

### Agent Response

> 🔍 Found 3 notes tagged #meeting-notes:
>
> 1. **Q1 Planning — Launch Pushed to April 15** — Mar 8
>    Decided to push launch, budget approved at $45k...
>
> 2. **Weekly Standup — Sprint 12 Retro** — Mar 5
>    Velocity down 15%, discussed blockers on auth redesign...
>
> 3. **Client Call — Acme Corp Onboarding** — Mar 3
>    Walked through integration timeline, API access granted...
>
> Want to see the full details on any of these?

---

## Scenario 3: Date + Topic Combined Search

### User Input

> Notes about the product launch from this week

### Agent Response

> 🔍 Found 2 notes matching "product launch" from this week:
>
> 1. **Product Launch Webinar Series** — Mar 8
>    Three-part webinar series idea: problem, demo, testimonials...
>
> 2. **Q1 Planning — Launch Pushed to April 15** — Mar 8
>    Launch date moved to April 15, budget $45k, ownership assigned...
>
> Want the full text on either?

---

## Scenario 4: Nothing Found

### User Input

> What did I note about cryptocurrency?

### Agent Response

> 🔍 No notes matching "cryptocurrency." Want me to capture something about it now?

---

## Scenario 5: Action Item Search

### User Input

> What do I need to do this week?

### Agent Response

> 📋 Open action items:
>
> 1. **Call Jake re: vendor contract** — Due: Friday (Mar 14)
>    From: Voice dump note, Mar 8
>
> 2. **Finalize copy** — Due: April 1
>    From: Q1 Planning meeting, Mar 8
>
> 3. **Schedule design review for Dashboard v2** — No due date
>    From: Product Roadmap Whiteboard, Mar 8
>
> Want me to mark any of these done?
