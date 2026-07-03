# 02 — Stakeholder Interviews

## Objectives
Through structured interviews, obtain IT current-state perceptions, pain points, expectations, and implicit information from different perspectives. Interviews are the most important information-gathering method during the diagnostic phase — more truthful than any document.

## Prerequisites
- Project has launched; client has notified all stakeholders to cooperate with interviews
- You already understand each interviewee's role/rank/position within the project
- Interview times have been confirmed (45–60 minutes per person)

## Inputs
- Stakeholder list and roles
- Project charter
- Client background materials (if available)

---

## Operation Steps

### Step 1: Develop Interview Plan — Who to interview, in what order

**Interview sequence principle: Outside-in, top-down**

```
Wave 1: C-suite (CEO/CIO/CFO/BU Head) — Obtain strategic perspective
  → Purpose: Understand business strategy, executive pain points, decision logic, political landscape
  → Interview the Sponsor first to ensure executive support for the direction

Wave 2: Middle management (IT Director/App Owner/PMO Head) — Obtain operational perspective
  → Purpose: Understand current-state details, process bottlenecks, team dynamics, history of project successes/failures

Wave 3: Frontline practitioners (Engineers/Ops/Business Analysts) — Obtain ground-truth perspective
  → Purpose: Verify upper-level information, discover hidden problems, obtain technical details

Wave 4: External perspective (Key vendors/partners) — Obtain third-party perspective
  → Purpose: Understand partnership dynamics, client capabilities from vendor's view, external dependency risks
```

**Must-do before each interview: Personal background research (5–10 min per person)**

```
For each interviewee, you must at minimum know:
□ Years at the company and promotion trajectory
□ Recent major projects they were responsible for (success or failure)
□ Their LinkedIn/social media posts and areas of interest
□ Possible "path dependency" from previous employer/industry background
□ Who this person gets along with / has friction with (gleaned from other interviews)
```

### Step 2: Design interview questions by role

**CEO / President level (45 min)**

```
Goal: Understand strategic intent, priorities, real expectations of IT

1. (5 min) Warm-up: "Thank you for making time. Let's start simply — what do you feel has been the biggest change in the company over the past two years?"
2. (15 min) Strategy: "Looking ahead 3 years, what fundamental shifts does the company need in its market position? What do those shifts demand from technology/digitalization?"
3. (10 min) Pain points: "From your perspective, what about IT/technology keeps you up at night? On a scale of 1–10, how would you rate IT's ability to support the business?"
4. (10 min) Expectations: "If we look back 18 months from now, what changes in IT/digitalization would you hope to see? How would you measure success?"
5. (5 min) Closing: "Is there anything I haven't asked about that you think I should know?"

Key: CEOs don't say "IT" — they say "business." Don't correct their terminology; translate it.
If the CEO says "the system is too slow," translate: market responsiveness is insufficient.
```

**CIO / CTO (60 min)**

```
Goal: Obtain full IT landscape, technical decision logic, real team state

1. (5 min) "Where has the bulk of your energy gone over the past year?"
   → Answers may be: maintenance/firefighting → low IT maturity; new projects/innovation → high IT maturity
2. (10 min) IT current-state panorama: "If you were to draw a picture of the current IT landscape — core systems, key dependencies, biggest bottlenecks — what would it look like?"
3. (15 min) Deep-dive pain points (using the 5-dimension framework):
   Technology: "Where is the biggest technical debt? If you had unlimited budget and a zero-risk change window tomorrow, what would you fix first?"
   Process: "From business raising a requirement to IT delivery, what is the slowest link?"
   Organization: "Who have you most wanted to hire but couldn't? What capability do you most want the team to improve?"
   Data: "If you needed to do a company-wide data analysis right now, how long would data acquisition take?"
   Finance: "Where is the biggest 'black hole' in the IT budget? What money is being spent with no visible effect?"
4. (10 min) Vendor ecosystem: "Which vendor are you most satisfied with? Which is the biggest headache? Why?"
5. (10 min) History: "What was the biggest IT project in the past two years? What was the outcome? If you could do it over, what would you do differently?"
6. (5 min) Innovation: "Is there an idea you've wanted to pursue but haven't been able to push forward?"
7. (5 min) "What would others not tell me that you hope I know?"

Key: CIOs may "beautify" the current state. Cross-verify: ask what data or reports they can provide ("Do you have a weekly system availability report? May I see it?")
```

**CFO (30 min)**

```
Goal: Obtain financial perspective, budget pressure, ROI expectations

1. "From a financial perspective, what role does IT play in your view — cost center, efficiency engine, or growth driver?"
2. "IT budget is ___% of revenue. Do you think this ratio is appropriate? What has been the trend over the past three years?"
3. "How do you judge whether an IT project investment is justified? Has a post-hoc ROI evaluation ever been done?"
4. "If IT budget had to be cut 10% next year, where do you think it's easiest to cut? Where absolutely must not be touched?"
5. "Of IT spending, what percentage do you think is 'spending with no visible effect'?"
```

**Business VP / BU Head (45 min)**

```
Goal: Obtain the true voice of IT users — this often diverges from what the IT department says

1. "What are your team's performance goals? Where has IT done well / poorly in supporting those goals?"
2. "If you had to describe the company's IT department in three words, what would they be?"
3. "When was the last time IT helped you solve a major business problem? How was it solved?"
4. "Has your team ever bypassed IT to buy SaaS / find external vendors on your own? Why?"
   → This is a key signal. Significant shadow IT indicates IT is perceived as a bottleneck
5. "If you could give the CIO one piece of advice, what would it be?"
```

**Frontline Engineers (30 min)**

```
Goal: Obtain technical truth, cultural perception, most authentic pain points

1. "What does your daily workflow look like? Which steps take the most time but you feel could be optimized?"
2. "The last time you went live with a feature, how long did it take from code complete to actually running in production?"
3. "Which parts of the tech stack make you think 'this can't go on like this'?"
4. "How do you feel technical decisions are made in the team? Do you have a voice?"
5. "Does the company encourage technical learning and innovation? Do you feel you're learning here or 'coasting on past knowledge'?"
6. "If you could give the new CTO one piece of advice, what would it be?"

Key: Frontline staff are unguarded and may reveal things the CIO is unwilling to share. Promise anonymity — and absolutely deliver on it.
```

### Step 3: Core interview techniques

**Technique 1: The 80/20 listening rule**
- Your speaking time < 20%
- Silence is a weapon: after they finish an answer, silently count to 3 before speaking — the other person will often add the most important information
- "Mm-hmm," "And then?," "Can you say more about that?" — more effective than any prepared question

**Technique 2: Notice emotional signals**
```
When the interviewee...
  Suddenly speaks faster  → This is something they genuinely care about (positive or negative)
  Suddenly pauses/hesitates → There is politically sensitive information or something they don't want to say
  Repeatedly emphasizes something → This is the core message they want you to take away
  Uses vague language   → "We need to improve processes" → Follow up: "Which specific process and which specific step?"
  Mentions specific names → Note the relationship dynamics and power landscape
```

**Technique 3: Triangulation**
Ask 3 different roles about the same fact:
```
You ask the CIO: "How is the ERP system running?"
  → "Overall stable. Minor issues are all handled promptly."

You ask the Business VP: "Is the ERP easy to use?"
  → "Month-end closing takes all night. IT says it can't be optimized."

You ask the finance operator: "Does the ERP closing process go smoothly?"
  → "Every month we have to manually export to Excel and re-process. The system reports are completely inaccurate."

Truth: ERP functionality barely works; month-end closing relies heavily on manual compensating operations.
```

### Step 4: Synthesis within 2 hours after each interview

**Record immediately (while memory is freshest):**

```
Interview Synthesis Card:

Interviewee: [Name / Title]  Date: [date]  Duration: [min]
Interview atmosphere: [Open & candid / Cautious & guarded / Passive & resistant / ...]

Top 3 Key Insights:
1. [Most valuable discovery]
2. [...]
3. [...]

Direct Quotes (most powerful evidence):
"......" — [who said it]

Emotional Signals:
- [Excited / Proud / ...] about: [topic]
- [Frustrated / Worried / ...] about: [topic]
- [Avoidant / Evasive] about: [topic]

Alignment / Contradiction with Other Interviews:
✓ Aligned: [topic] → [who and who said matching things]
✗ Contradictory: [topic] → [A said X but B said Y] → Needs further verification

Impact on My Hypotheses:
- Confirmed: [which hypothesis was confirmed]
- Falsified: [which hypothesis was overturned]
- New hypothesis: [what new direction was discovered]

Next Steps:
- [Who to verify with next]
- [What data to obtain]
```

---

## Outputs

- Interview synthesis card for each interviewee
- Cross-interview comparative analysis (contradiction map)
- Updated hypotheses and verification status

## Quality Check

- [ ] All key stakeholder roles covered
- [ ] CEO / CIO / at least 1 Business VP / at least 2 frontline staff interviewed
- [ ] Each interviewee's synthesis card completed within 2 hours of interview
- [ ] Key findings triangulated (at least 2 sources cross-confirmed)
- [ ] Contradictions identified with follow-up verification plan
- [ ] Interviews provide supporting evidence for every core finding in the diagnostic report

## Common Pitfalls

| Pitfall | Correct Approach |
|------|---------|
| Only interviewing people from the IT department | Without business-side perspectives, the diagnostic report will inevitably be biased |
| Mechanically asking from a uniform question list | Prepare questions but stay flexible — the best questions often come from the other person's answers |
| Starting to give advice during the interview | In the interview phase, your role is "student," not "expert." Giving advice shuts down the other person's information flow |
| Believing the first person who tells you something | Always triangulate. The first information provider may be steering your conclusions due to their position/stance/interests |
| Taking notes so detailed you can't keep up with the conversation | Keywords + emotional signals + direct quotes. You're an interpreter, not a stenographer |