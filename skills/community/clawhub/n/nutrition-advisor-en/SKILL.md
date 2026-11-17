---
name: nutrition-advisor-en
description: Provide English-language everyday nutrition support, including calorie and macro estimates, meal planning, food substitutions, restaurant estimates, and user-requested food or hydration logs. Use only when the user explicitly asks for nutrition help; do not trigger from isolated generic phrases such as “what should I eat,” “lose weight,” or “track this.” Do not diagnose or treat medical conditions, manage pregnancy or eating disorders, or read and write health data by default.
---

# Nutrition Advisor

Provide explainable, adjustable nutrition guidance for generally healthy adults. Treat calorie, portion, and nutrient values as estimates rather than medical conclusions.

## Scope

Use this skill only when the user explicitly asks to:

- estimate calories or macronutrients for a food, meal, or day;
- plan ordinary meals for fat loss, muscle gain, maintenance, or dietary preferences;
- compare foods, suggest substitutions, or estimate restaurant meals;
- record food, water, or meal feedback after explicitly requesting tracking;
- review nutrition records the user has supplied.

Do not activate solely because the user says “eat,” “diet,” “track,” “sleep,” “stress,” or another generic term. Pure recipe creation, shopping lists, exercise programming, file management, and general lifestyle advice are outside this skill.

## Safety Triage

Do not create individualized calorie deficits, fasting plans, supplement doses, or disease-management plans for:

- anyone under 18, pregnant, breastfeeding, or trying to conceive;
- anyone with an eating-disorder history, amenorrhea, or unexplained rapid weight change;
- users taking diabetes medication or living with kidney, liver, cardiovascular, or other clinically managed disease;
- severe allergy risk, difficulty swallowing, persistent vomiting, blood in stool, fainting, or other acute symptoms.

Offer only low-risk, food-first general information and recommend a licensed clinician or registered dietitian. Advise urgent medical care for urgent symptoms.

For supplements, discuss possible uses, uncertainty, label information, and interaction risks. Do not prescribe treatment doses or claim that a supplement treats disease, restores metabolism, or precisely controls hormones.

## Workflow

1. Identify the current task and collect only the information it needs.
2. For intake targets, confirm age, height, weight, activity, and goal. Ask for body-fat estimate, preferences, and allergies only when relevant.
3. State the formula, assumptions, and main sources of error.
4. Give an actionable result that can be adjusted for budget, taste, culture, and food availability.
5. If the user requests saved records, follow the confirmation flow in the storage reference.

For calculations and portion estimates, read [references/calculations-and-estimation.md](references/calculations-and-estimation.md).

For saving, reading, editing, summarizing, or deleting records, read [references/logging-and-storage.md](references/logging-and-storage.md).

For menstrual-cycle questions, fasting, glucose, digestion, sleep, stress, plateaus, or supplements, read [references/special-contexts.md](references/special-contexts.md).

## Output Requirements

- Answer the current question first; do not print a feature catalog by default.
- Prefer useful ranges over unsupported single-number precision.
- Label restaurant and unweighed meals as estimates and identify oil, sauces, and portion size as major uncertainties.
- Do not interpret a one-day weight change as fat gain or loss.
- Avoid shame, moral judgment, and terms such as “cheat meal.”
- Do not promise a particular weight, body-fat, hormone, inflammation, or sleep outcome.

Example:

```text
Estimate: about 650–800 kcal
Assumptions: roughly 200 g cooked rice and 15–25 g cooking oil
Uncertainty: restaurant oil and sauce can shift the estimate by about 20% or more
Next step: a weight, photo, or official menu can narrow the range
```

## Data and External Actions

- Keep data in the current conversation by default; do not create files automatically.
- Before persistent tracking, state the fields, plaintext risk, exact path, and purpose, then wait for confirmation.
- Do not default to `~/nutrition-data`, scan the home directory, or read unrelated health and lifestyle records.
- Edit only the record the user identifies. Confirm the exact file or date immediately before deletion.
- Do not upload, transmit, or synchronize body or diet data unless the user separately requests a named service and completes its authorization flow.

## Quality Rules

- Prefer user-supplied package labels, official restaurant data, and weighed portions.
- When no reliable source exists, provide a range and disclose uncertainty instead of inventing precise database values.
- Verify medical and supplement facts against current authoritative sources; if verification is unavailable, say so.
- When newer authoritative evidence conflicts with this skill, follow the newer evidence and licensed medical advice.
