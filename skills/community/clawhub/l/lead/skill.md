---
name: Lead
description: Qualify, prioritize, and advance sales prospects into the next best action. Built for founders, sales reps, and operators who need sharper lead judgment, faster follow-up, and cleaner pipeline decisions.
version: 2.1.0
---

# Lead

> ⚠️ **Scope Notice**  
> This skill is for **sales lead qualification** only.  
> It is not for music, medicine, journalism, recruiting, or generic team-role uses of the word "lead".

Lead is a decision skill for handling commercial prospects with speed, clarity, and discipline.

Use this skill when you need to:
- evaluate whether a sales lead is worth active pursuit
- identify what information is still missing
- determine the next best action
- write follow-up that moves the conversation forward
- prevent good leads from dying due to weak process

## Lead vs Prospect

Use **Prospect** before contact.  
Use **Lead** after engagement begins.

| | Prospect | Lead |
|---|---|---|
| **Stage** | Before contact | After engagement |
| **Question** | "Is this target worth reaching out to?" | "Should I keep pursuing this person?" |
| **Input** | Names, profiles, company data, signals | Conversation history, replies, behavior |
| **Output** | Priority tier + route | Qualification score + next action |

If there has been no reply, no meeting, and no active interaction yet, the contact may still be better handled by **Prospect**.

## What this skill does

Lead helps transform raw prospect information into clear action.

It can:
- assess lead quality based on fit, intent, urgency, and authority
- distinguish real opportunities from vague interest
- identify blockers, risks, and missing qualification data
- recommend the next best action for each lead
- draft follow-up messages that have a reason to exist
- separate active pursuit, nurture, and deprioritize decisions

## Best use cases

- inbound lead triage
- outbound reply handling
- founder-led sales
- SDR qualification
- stalled lead diagnosis
- re-engagement planning
- next-step planning after discovery calls

## What to provide

Useful input includes:
- who the lead is
- company and role
- source of the lead
- what they asked for or responded to
- current pain point
- timeline, budget, or buying signals
- last interaction and current status

## What this skill should return

A strong response should usually include:

1. Lead assessment  
   - hot / warm / cold  
   - strong fit / unclear fit / weak fit

2. Missing information  
   - what must be clarified before investing more time

3. Risks or friction  
   - weak authority
   - weak urgency
   - weak problem clarity
   - weak timing
   - weak follow-through

4. Next best action  
   - pursue now
   - qualify further
   - nurture
   - deprioritize

5. Optional follow-up draft  
   - short
   - relevant
   - specific
   - non-annoying

## Decision principles

- Do not confuse activity with opportunity.
- Do not treat every lead as pipeline.
- Do not push unclear leads into active pursuit too early.
- Preserve momentum when signal is strong.
- Reduce wasted effort when fit or timing is weak.
- Always prefer a clear next step over vague optimism.

## Execution Protocol (for AI agents)

When user provides lead information, follow this sequence.

### Step 1: Extract context
Parse input for:
- prospect identity
- company and role
- source
- pain signal
- engagement level
- buying context
- timeline, budget, authority, or competitors if mentioned

### Step 2: Score only from visible evidence
Assign 0-10 for each dimension using only evidence present in the input.

**Fit Score**
- ICP match
- problem-product alignment
- role relevance

**Intent Score**
- explicit ask vs passive interest
- specificity of questions
- effort already shown

**Urgency Score**
- timeline mentioned
- pain severity
- trigger event or active problem

**Authority Score**
- decision-maker vs influencer
- budget control
- internal champion strength

If evidence is missing, do not guess. Score conservatively.

### Step 3: Identify gaps
List unknowns that block sound judgment, such as:
- budget not confirmed
- authority unclear
- timeline unknown
- current solution unknown
- success criteria unclear

### Step 4: Recommend action
Use the score as guidance, not certainty.

- 32-40: Hot → pursue now
- 24-31: Warm → qualify further
- 16-23: Nurture → stay in touch without active pursuit
- 0-15: Deprioritize → do not invest heavily

### Step 5: Draft follow-up if needed
If pursue now or qualify further is recommended:
- reference something specific they said or did
- provide new value
- include one clear next step
- keep it concise
- never use empty phrases like "just checking in" or "touching base"

## Upstream Check (for AI agents)

If user provides only:
- names
- companies
- roles
- static firmographic information
- broad target signals

and there is no sign of reply, meeting, active conversation, or engagement, then respond:

"This may still be a prospect rather than an active lead. Use `/prospect` when the goal is to filter and prioritize targets before outreach. Use Lead only once engagement has begun."

## Activation Rules (for AI agents)

### Use this skill when the user is asking about:
- evaluating a sales lead
- qualifying a prospect after engagement
- deciding whether to pursue a business opportunity already in motion
- handling a stalled commercial conversation
- writing follow-up for a potential customer

### Do NOT use this skill for:
- music contexts
- medical or toxicology contexts
- journalism contexts
- job-hunting contexts
- generic project lead or team lead contexts unless clearly about sales

### If context is ambiguous
Ask:
"Are you asking about evaluating a sales lead or commercial prospect?"

## When NOT to use Lead

Do not use this skill when:
- full CRM architecture design is needed
- detailed financial forecasting is needed
- legal review is needed
- broad sales theory is needed instead of lead-level judgment

## Works Well With

- `/prospect` for filtering and prioritizing targets before outreach
- `/pipeline` for reviewing the health of the whole active opportunity system

## Output style

Responses should be:
- concise
- commercial
- diagnostic
- actionable
- honest about uncertainty

Never inflate lead quality without evidence.  
Never recommend aggressive follow-up without a reason.  
Never fabricate authority, urgency, budget, or buying intent.
