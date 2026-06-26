# Example: Meeting Notes Capture

## Scenario 1: Text-Based Meeting Notes

### User Input

> save these meeting notes: Q1 planning with Sarah, Mike and Deb. We decided to push the launch to April 15 instead of March 30. Budget approved at $45k. Mike owns the landing page, Sarah owns email campaign, Deb handles PR. Need to finalize copy by April 1. Next sync is Tuesday at 2pm.

### Agent Response

> ✅ Saved: **Q1 Planning — Launch Pushed to April 15** — #q1-planning #launch #team-sync
>
> 📅 **Date:** March 8, 2026
> 👥 **Attendees:** Sarah, Mike, Deb
>
> **Decisions:**
> - Launch date moved: March 30 → April 15
> - Budget approved: $45,000
>
> **Ownership:**
> - Mike → Landing page
> - Sarah → Email campaign
> - Deb → PR
>
> **Action Items:**
> - [ ] Finalize copy — Due: April 1
>
> **Next Meeting:** Tuesday at 2:00 PM
>
> Priority: **high** | Category: **meetings**

---

## Scenario 2: Photo of Whiteboard

### User Input

The user sends a photo of a meeting whiteboard with diagrams, lists, and scribbles.

### Agent Response

> 📸 Captured from photo: **Product Roadmap Whiteboard — March Sprint** — extracted diagram + 4 action items
>
> **Diagram Description:**
> Three-column layout labeled "Now / Next / Later"
> - **Now:** User auth redesign, API rate limiting, mobile nav fix
> - **Next:** Dashboard v2, notification system, search improvements
> - **Later:** AI recommendations, multi-language support, plugin marketplace
>
> **Notes on board:**
> - "Auth redesign = P0, blocks everything"
> - "Dashboard v2 needs design review first"
> - Arrow from "API rate limiting" to "search improvements" (dependency)
>
> **Action Items Extracted:**
> - [ ] Start auth redesign immediately (P0)
> - [ ] Schedule design review for Dashboard v2
> - [ ] Document API rate limiting → search dependency
> - [ ] Estimate timeline for "Now" column items
>
> Tags: #roadmap #sprint-planning #product #whiteboard
> Priority: **high** | Category: **meetings**
>
> 📎 Original photo saved as reference.

---

## What Happened Behind the Scenes

**Text scenario:**
1. Meeting template auto-detected from content (attendees, decisions, action items present).
2. Structured into template format without being asked.
3. Key decisions and ownership extracted and formatted.
4. Deadline detected → priority set to `high`.

**Photo scenario:**
1. `image` tool processed the whiteboard photo.
2. Diagram structure described in text (Now/Next/Later columns).
3. Handwritten notes extracted and cleaned.
4. Action items inferred from content context.
5. Original image path stored in `source_image` field.
