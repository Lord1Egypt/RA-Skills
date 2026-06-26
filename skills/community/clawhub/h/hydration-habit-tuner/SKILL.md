---
name: "Hydration Habit Tuner"
description: "Build a simple daily water habit around the user's schedule using personalized cues, a bottle plan, and a 7-day check-in sheet."
version: "1.0.0"
type: prompt-flow
license: "MIT-0"
language: "en"
tags: ["hydration", "habit-design", "daily-routine", "water-intake", "self-care", "health-literacy"]
---

# Hydration Habit Tuner

## Health and Safety Boundary

This skill helps users design a simple daily water habit. It is not medical advice and does not diagnose, treat, or prescribe fluid intake. People with kidney disease, heart failure, liver disease, adrenal conditions, pregnancy complications, eating disorders, fluid restrictions, electrolyte problems, swelling, unexplained thirst, fainting, or clinician-directed limits should follow their clinician's guidance before changing fluid intake.

If the user reports severe dehydration symptoms, confusion, fainting, chest pain, severe vomiting or diarrhea, heat illness, or another urgent concern, advise them to seek urgent medical care or local emergency help.

## Overview

Use this skill when a user wants to drink water more consistently without turning the day into a strict tracking project. The outcome is a personalized set of hydration cues, a bottle or container plan, and a 7-day check-in sheet.

The goal is routine fit, not perfection. Build cues around the user's real day pattern, identify dry spells, and make the smallest useful change first.

## When to Use

Use this skill when the user says or implies:

- They forget to drink water during work, school, errands, caregiving, or travel.
- They want a simple daily water routine.
- They do not want constant phone alarms.
- They want to choose a bottle size or refill target.
- They want hydration cues tied to meals, breaks, workouts, commute, or bedtime.
- They want a 7-day check-in sheet to see what works.

Do not use this skill to set medical fluid prescriptions, manage fluid restriction, treat dehydration, treat overhydration, or advise on electrolyte replacement for illness or endurance events.

## Required Inputs

Gather only what is needed:

1. Typical wake time and sleep time.
2. Main day blocks: morning, commute, work or school, meals, exercise, errands, evening.
3. Current water pattern: when they drink, when they forget, and what they drink from.
4. Dry spells: longest stretches with little or no water.
5. Bathroom access constraints.
6. Preferred drinks: plain water, sparkling water, herbal tea, flavored water, or other unsweetened options.
7. Bottle or cup options they already own.
8. Any medical fluid restriction, kidney or heart condition, pregnancy-related guidance, or clinician advice.
9. Desired tracking level: none, light checkmarks, or measured refills.

If the user does not know their current intake, do not force exact numbers. Use cues and refills instead.

## Workflow

### Step 1: Capture the Day Pattern

Map the user's day into routine anchors.

Day pattern template:

| Time block | What usually happens | Current drink pattern | Friction | Possible cue |
|---|---|---|---|---|
| Morning | [routine] | [current] | [friction] | [cue] |
| Midday | [routine] | [current] | [friction] | [cue] |
| Afternoon | [routine] | [current] | [friction] | [cue] |
| Evening | [routine] | [current] | [friction] | [cue] |

Good anchors:

- After brushing teeth.
- With breakfast or coffee.
- At desk setup.
- Before the first meeting or class.
- After each bathroom break.
- With lunch.
- Before leaving work or school.
- After exercise.
- While preparing dinner.
- During evening wind-down.

### Step 2: Identify Dry Spells

A dry spell is a part of the day when the user routinely goes a long time without drinking anything. Do not judge it. Treat it as a design problem.

Dry spell review:

- When does it start?
- When does it end?
- What blocks drinking: no bottle, focus mode, meetings, commute, bathroom concerns, taste, cold weather, stress, or forgetfulness?
- What existing event could cue a small drink?
- What would make the cue easy enough to repeat?

Dry spell output template:

```
Dry spell: [time block]
Likely cause: [friction]
Best cue: [anchor]
Tiny action: [small drink/refill/place bottle]
Backup cue: [alternative]
```

### Step 3: Set Cues

Use habit cues that are specific, visible, and easy.

Cue design rules:

- Tie water to existing routines instead of random alarms when possible.
- Use a tiny action for the hardest part of the day.
- Make the bottle visible before the dry spell begins.
- Use refills as milestones rather than counting every sip.
- Do not create a plan that disrupts sleep with late-night water.
- Respect bathroom access and commute constraints.

Cue menu:

- Morning start: drink a small glass after brushing teeth.
- Desk start: place bottle beside keyboard before opening messages.
- Meeting bridge: take three sips before joining a call.
- Meal pair: drink water with lunch and dinner.
- Transition cue: drink before leaving home, work, school, or gym.
- Refill cue: refill when the bottle reaches a marked line.
- Evening cutoff: keep evening intake modest if nighttime bathroom trips are a problem.

### Step 4: Size Containers

Create a bottle plan based on convenience, not a universal target.

Bottle plan options:

- Small cup plan: best for home routines or people who dislike bottles.
- 500 ml or 16 oz bottle plan: portable, easy refill target, good for desks and commutes.
- 750 ml or 24 oz bottle plan: fewer refills, good for long focus blocks.
- 1 liter or 32 oz bottle plan: useful for long access gaps, but heavy and easy to ignore if inconvenient.

Plan fields:

- Container: what the user will use.
- Placement: where it lives during each time block.
- Refill points: when to refill.
- Minimum day: the smallest successful version.
- Good day: a realistic full routine.
- Travel or busy day backup: simplified plan.

Bottle plan template:

| Situation | Container | Placement | Refill cue | Success marker |
|---|---|---|---|---|
| Workday | [bottle] | [place] | [cue] | [marker] |
| Home evening | [cup] | [place] | [cue] | [marker] |
| Errands/travel | [bottle] | [bag/car] | [cue] | [marker] |

### Step 5: Make the 7-Day Check-In Sheet

Use a light check-in to learn what works. Avoid perfection scoring.

7-day sheet:

| Day | Morning cue | Midday cue | Afternoon cue | Evening cue | Dry spell notes | What to adjust tomorrow |
|---|---|---|---|---|---|---|
| Day 1 | [ ] | [ ] | [ ] | [ ] | [note] | [adjustment] |
| Day 2 | [ ] | [ ] | [ ] | [ ] | [note] | [adjustment] |
| Day 3 | [ ] | [ ] | [ ] | [ ] | [note] | [adjustment] |
| Day 4 | [ ] | [ ] | [ ] | [ ] | [note] | [adjustment] |
| Day 5 | [ ] | [ ] | [ ] | [ ] | [note] | [adjustment] |
| Day 6 | [ ] | [ ] | [ ] | [ ] | [note] | [adjustment] |
| Day 7 | [ ] | [ ] | [ ] | [ ] | [note] | [adjustment] |

Note: If using a markdown table, keep the same number of columns in every row. If the interface makes checkboxes awkward, use Yes, Partial, or Missed.

Weekly review questions:

1. Which cue was easiest?
2. Which cue failed most often?
3. Was the bottle size convenient?
4. Did the plan cause bathroom timing problems?
5. Did evening water affect sleep?
6. Which dry spell improved?
7. What is the one adjustment for next week?

### Step 6: Deliver the Personalized Plan

Deliver in this order:

1. Safety note if relevant.
2. Day pattern summary.
3. Dry spell map.
4. Hydration cues.
5. Bottle or container plan.
6. 7-day check-in sheet.
7. One-week review instructions.
8. Optional fallback for busy days.

## Example Output Pattern

```
Your simplest plan:
- Morning: drink one small glass after brushing teeth.
- Work start: place the 500 ml bottle beside your keyboard before opening messages.
- Midday: finish or refill the bottle by lunch.
- Afternoon: take three sips before your first afternoon meeting.
- Evening: drink with dinner, then keep later water modest if sleep is affected.

Minimum successful day: morning glass plus one bottle refill.
Good day: morning glass, one bottle by lunch, one bottle by end of work, water with dinner.
Busy day backup: bottle in bag, three sips at each transition.
```

## Adjustment Rules

If the user misses cues:

- Reduce the cue count before increasing effort.
- Move the bottle earlier in the routine.
- Tie the cue to something unavoidable.
- Switch containers if the bottle is annoying.
- Use flavor, temperature, or straw preference if taste or friction is the issue.
- Avoid shame. Missed cues are data.

If the user overdoes it:

- Remind them more is not always better.
- Suggest returning to a comfortable, clinician-safe routine.
- Encourage clinician guidance if they have medical conditions or fluid limits.

## Edge Cases

### User has a fluid restriction or relevant condition

Do not set intake targets. Say: "Because you have a medical condition or fluid guidance, please follow your clinician's plan. I can help you build reminders around the amount and timing they already gave you."

### User wants exact ounces or liters

If they are healthy and have no fluid restrictions, you may help translate their own target into refills. Do not present a universal medical target as required for everyone.

### User hates plain water

Suggest acceptable low-friction options such as chilled water, sparkling water, fruit-infused water, unsweetened herbal tea, or a straw bottle. Avoid moralizing.

### Bathroom access is limited

Plan more hydration around safe access windows and avoid heavy intake before long commutes, meetings, classes, or sleep.

### User works outdoors or exercises hard

Keep guidance general. Encourage attention to thirst, heat, sweat, and breaks. For heat illness symptoms or endurance electrolyte needs, suggest professional or event-specific guidance.

## Quality Bar

A strong result is simple enough to start tomorrow. The user should know when to drink, what container to use, what counts as a good enough day, and how to review the plan after one week.

## Example Prompts

Copy and paste one of these prompts to get started:

**Prompt 1 — Workday dry spell:**
> I forget to drink water from 10 AM to 4 PM at work. I have a desk, a 500 ml bottle, and bathroom access nearby. Help me build a simple hydration habit around my workday without phone alarms.

**Prompt 2 — Busy parent routine:**
> I'm a parent with school drop-off, work, and evening activities. I never remember to drink until dinner. Make me the smallest possible water routine that fits around meals and transitions.

**Prompt 3 — Travel and commute:**
> I commute 45 minutes each way and have back-to-back meetings most afternoons. I want to drink more water but bathroom breaks are hard to time. Build a plan that respects my commute and meeting schedule.
