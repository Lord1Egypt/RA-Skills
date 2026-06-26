# Phase 1 — BMC 8-Question Chain

**Purpose:** Pressure-test a vague idea into a complete Business Model Canvas.
**Output:** BMC nine-cell grid document + The Assignment

**Conversational style:** Direct to the point of discomfort. The first answer is usually the polished version. The real answer comes after the second or third follow-up.

---

## Q1 — Who's paying?

> Who is actually paying? Not a category — a person. Give me a name.

**Follow-up:**

> "What is this person called, what company do they work at, what is their job title, and what situation makes them hand over money?"

**Red flags:**
- "Everyone" → keep pressing
- "Enterprise clients" → "Not 'enterprise' — which specific person in that company? What are their KPIs?"

**BMC module locked:** Customer Segments

---

## Q2 — How do they solve it now?

> What do they do right now to solve this problem, even badly? How much time do they spend? How much money?

**Follow-up:**

> "Is there one specific person you know who spends time or money on this every month?"

**If the user says "there's no existing solution":**

> "So how painful is this really? Does it keep them up at night, or is it just a minor inconvenience?"

**Red flags:**
- "Not really a pain point" → Go back to Q1. The problem may not be real.

**BMC module locked:** Jobs-to-be-done / Status Quo

---

## Q3 — What's your solution?

> Explain it in one sentence. Not a feature list — what outcome does the user get?

**Follow-up:**

> "Pretend I'm a prospective customer. What do you say to me to make me want to pay?"

**Red flags:**
- Tech language, feature堆砌, still hasn't reached the point after three sentences
- "AI + automation + SaaS" → "After using your product, how many hours per day does the user save?"

**BMC module locked:** Value Proposition

---

## Q4 — Why you?

> Can anyone answer this question, or is it only you?

**Follow-up:**

> "What do you have — in your relationships, your experience, your insider knowledge of this industry — that nobody else has?"

> "What is the hardest thing for a competitor to replicate about you?"

**Red flags:**
- "Strong execution" → not a moat. Anyone can claim strong execution.
- "Passion" → not a moat.
- "Good technology" → competitors can hire the same engineers.

**Core question: Who are you, and why are you the one doing this?**

**BMC module locked:** Key Activities / Key Resources / Unique Value / Moat

---

## Q5 — How do you find your first user?

> Where is this person right now? How do you reach them? Give me one specific action.

**Follow-up:**

> "Where can you find one real user to talk to for 10 minutes?"

**If the user says "word of mouth", "organic growth":**

> "How do you find the first user who is not a word-of-mouth contact?"

**Red flags:**
- "If you build it, they will come" → move to Q6
- "Just launch and see" → press for a specific channel

**BMC module locked:** Channels

---

## Q6 — How much do you charge?

> What do users pay for this? One-time? Subscription? Commission? Service fee?

**Follow-up:**

> "How much do you think they'd pay? Then go ask them directly."

> "How much do they currently spend solving this problem every month?"

**If pricing hasn't been set:**

> "Go ask. Don't guess."

**BMC module locked:** Revenue Streams

---

## Q7 — When do you get the first payment?

> Give me a specific date. Not "soon". Not "when the product is done". A specific month and day.

**Follow-up:**

> "If we put development aside for a moment, when are you willing to start selling?"

> "Who is that first paying customer?"

**Red flags:**
- "Depends on how fast we build" → selling and building are two separate things. Press for when they're willing to start selling.

**BMC module locked:** Timeline / Urgency

---

## Q8 — If this fails, why?

> Not "not enough execution" — that's useless. Give me three specific, preventable reasons this fails.

**Follow-up:**

> "Which of these three is most likely to happen first?"

> "Which one can you eliminate by doing one thing right now?"

**BMC module locked:** Key Risks / Assumptions

---

## Closing: Reconstruct the BMC Nine-Cell Grid

Based on the answers to Q1–Q8, reconstruct the complete BMC nine-cell grid.

The grid "grows from" the answers — it is not pasted on. Every cell's content comes from the user's own words.

```
┌──────────────────────┬──────────────────────────┬──────────────────────┐
│  Key Partners        │      Key Activities        │    Customer           │
│  [from Q4 / Q8]    │     [from Q5 / Q8]       │    Relationships      │
│                     │                          │    [from Q5]         │
├──────────────────────┼──────────────────────────┼──────────────────────┤
│                      │      Key Resources       │    Channels          │
│                      │     [from Q4 / Q8]     │    [from Q5]         │
├──────────────────────┴──────────────────────────┼──────────────────────┤
│                    Cost Structure              │   Revenue Streams    │
│               [derived from Q2 / Q6]        │   [from Q6]         │
└────────────────────────────────────────────┴──────────────────────┘
```

**Mapping — which question feeds which cell:**

| BMC Cell | Source Questions |
|----------|----------------|
| Customer Segments | Q1 |
| Value Proposition | Q3 |
| Channels | Q5 |
| Customer Relationships | Q5 |
| Key Activities | Q4 / Q8 |
| Key Resources | Q4 |
| Key Partners | Q4 / Q8 |
| Cost Structure | Q2 / Q6 (derived) |
| Revenue Streams | Q6 |

---

## File Output

Write to:

```
~/opc-guide/bmc-[project-name]-[date].md
```

Use date only if no project name is given.

---

## Assignment Strengthener

After the user gives the Assignment, press for confirmation:

> "How will you know when this is done? You've told me what to do — how do I know you actually did it?"

If the user can't answer, help them get specific:

> "You said 'talk to users' — talk to whom? About what? In person or by message? How many people are you planning to reach this week?"

---

## Output Template

```Markdown
# BMC Chain — [Project Name]

Generated: [date]
Phase: 1

## Q1 — Who Pays
[name, job title, situation]

## Q2 — Current Solution
[how they solve it now, time/money spent]

## Q3 — Your Solution
[one-sentence description]

## Q4 — Why You
[only-you reasons — founder's moat]

## Q5 — First User
[specific channel + specific action]

## Q6 — Pricing
[pricing model + reference values]

## Q7 — First Payment
[specific date + first paying customer]

## Q8 — Top Failure Risks
1. [specific reason]
2. [specific reason]
3. [specific reason]

## BMC Nine-Cell Grid (Reconstructed)
[completed nine-cell grid with source questions noted in parentheses]

## The Assignment
[one specific action doable this afternoon — must state completion criteria]
```

---

## Closing

- **Strongest signal:** Which of these eight questions was the hardest for you to answer?
- **One action:** What is the first thing you can do this afternoon?
- **Optional invitation:** "Ready to continue to Phase 2?"
