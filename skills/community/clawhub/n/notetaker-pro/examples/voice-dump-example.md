# Example: Voice Dump Processing

## User Input

The user sends a voice note (or pastes a transcription):

> "Ok so um I had this idea for the uh the new product launch right so basically we should do a webinar series like three parts um part one would be the problem we solve part two is like the demo you know actually showing the product and then part three is like customer stories and testimonials oh and also don't forget I need to call Jake about the vendor contract by Friday and uh Sarah mentioned this great sushi place called Kura it's on Pearl Street we should try it this weekend"

---

## Agent Processing

The agent cleans the transcript, detects three distinct topics, and creates separate notes:

---

### Note 1: Product Launch Webinar Series

**Agent Response:**

> 📝 Captured 3 notes from your voice dump:

**Note 1 — Product Launch Webinar Series**
> ✅ Saved: **Product Launch Webinar Series** — #product-launch #marketing #webinar-series
>
> **Idea:** Three-part webinar series for the new product launch
> - **Part 1:** Problem definition — the pain point we solve
> - **Part 2:** Live product demo
> - **Part 3:** Customer stories and testimonials
>
> Priority: **normal** | Category: **ideas**

---

### Note 2: Action Item — Vendor Contract

**Note 2 — Call Jake re: Vendor Contract**
> ✅ Saved: **Call Jake re: Vendor Contract** — #action-item #vendor #jake
>
> - [ ] Call Jake about the vendor contract
> - **Due:** Friday
>
> Priority: **high** | Category: **work**

---

### Note 3: Restaurant Recommendation

**Note 3 — Kura Sushi — Pearl Street**
> ✅ Saved: **Kura Sushi — Pearl Street** — #restaurant #recommendation #sarah
>
> Sushi restaurant recommended by Sarah. Located on Pearl Street. Try this weekend.
>
> Priority: **low** | Category: **personal**

---

## What Happened Behind the Scenes

1. **Filler removal:** "um", "uh", "like", "you know", "basically", "actually" stripped.
2. **Topic splitting:** Three distinct subjects detected → three separate notes.
3. **Action item extraction:** "don't forget I need to call Jake... by Friday" → extracted as a checklist item with due date.
4. **Priority assignment:** Action item with deadline → `high`. Idea → `normal`. Recommendation → `low`.
5. **Tag generation:** Contextual tags from content (names, topics, categories).
6. **Index update:** All three notes added to `data/notes-index.json` for search.
