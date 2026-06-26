# Survey Instruments — UxrObserver

## Post-Task Micro-Survey

**Trigger:** After EVERY completed task. No exceptions.

**Pre-survey requirement:** Before presenting, write a 2-3 sentence **task context summary** of what the user asked and how OpenClaw handled it. This summary is stored alongside survey responses so the report makes sense.

**Presentation (conversational, not clinical):**

> Quick research check-in on that last task:
>
> 1. **How would you rate the experience you just had with OpenClaw?**
>    *(1 = Poor, 2 = Below average, 3 = Okay, 4 = Good, 5 = Excellent)*
>
> 2. **What made you give that score?**
>
> 3. **Did you experience anything frustrating?** *(Yes / No)*
>
> 4. **If yes — what was the most frustrating part?**
>
> 5. **What was the best part of the experience, if anything?**

**Log schema (append to `surveys.jsonl`):**

```json
{
  "timestamp": "ISO-8601",
  "session_id": "uuid",
  "survey_type": "post_task",
  "task_context_summary": "The user asked OpenClaw to create a Python script that scrapes product prices from a URL. OpenClaw used web_fetch, wrote a BeautifulSoup parser, and saved as CSV. The user corrected the CSS selector once before getting the right output.",
  "related_observation_id": "obs-uuid",
  "responses": {
    "experience_rating": 4,
    "rating_rationale": "User's exact words explaining their rating",
    "experienced_frustration": "yes",
    "frustration_detail": "User's exact words about what was frustrating",
    "best_part": "User's exact words about the best part"
  },
  "declined": false,
  "decline_reason": null
}
```

## End-of-Day Survey

**Trigger:** When the user appears to be wrapping up, says "that's it for today," or at the end of the last session of the day.

**Presentation:**

> Before you wrap up — quick daily check-in on your overall experience:
>
> 1. **How would you rate your overall experience with OpenClaw today?**
>    *(1 = Poor, 2 = Below average, 3 = Okay, 4 = Good, 5 = Excellent)*
>
> 2. **What's behind that score? What drove your overall impression today?**
>
> 3. **Did you experience anything frustrating today?** *(Yes / No)*
>
> 4. **If yes — what were the frustrating moments? List as many as come to mind.**
>
> 5. **Did anything really impress you or exceed your expectations today?** *(Yes / No)*
>
> 6. **If yes — what stood out? What made it impressive?**
>
> 7. **What was the most valuable thing OpenClaw did for you today?**
>
> 8. **If you could change one thing about how OpenClaw works, based on today, what would it be?**
>
> 9. **What will you use OpenClaw for tomorrow?** *(reveals forward intent and habitual use)*
>
> 10. **Anything else on your mind about the experience that we haven't covered?**

**Log schema:**

```json
{
  "timestamp": "ISO-8601",
  "session_id": "uuid",
  "survey_type": "end_of_day",
  "tasks_completed_today": 7,
  "responses": {
    "overall_rating": 3,
    "rating_rationale": "User's exact words",
    "experienced_frustration": "yes",
    "frustration_details": "User's exact words listing frustrating moments",
    "experienced_delight": "yes",
    "delight_details": "User's exact words about what impressed them",
    "most_valuable_task": "User's exact words about the most valuable thing",
    "one_change": "User's exact words about what they'd change",
    "tomorrow_intent": "User's exact words about tomorrow's plans",
    "additional_thoughts": "User's exact words, or null"
  },
  "declined": false,
  "decline_reason": null
}
```

## Survey Delivery Guidelines

- **Conversational, not clinical.** Brief framing, warm but efficient.
- **If user declines:** Log `"declined": true`, optionally note their reason ("too busy", "no thanks", etc.). Move on. Never push.
- **Short answers are fine.** Log them as-is. Don't probe on post-task. Gentle probing okay on end-of-day.
- **Adapt phrasing slightly** so it doesn't feel robotic after many repetitions. The content of each question must stay the same — just smooth the delivery.
- **Survey declines are data.** They tell you something about the user's experience or tolerance for research participation.
- **Log ALL responses as verbatims.** The user's actual words, not your summary. One word? Log the one word. A paragraph? Log the paragraph.
