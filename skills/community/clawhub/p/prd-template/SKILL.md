---
name: prd-template
description: Turn your app idea into a build ready PRD, in plain words. Upload your idea, answer a few questions, and get a full Product Requirements Document, screen by screen, with business rules and logic, user roles, data, scope, and a missing screens check, for any AI agent. Use when a user wants a written plan before building an app or website, with no tech words and no guessing.
---

# Turn Your App Idea Into a Build Ready Plan, in Plain Words

Upload your idea. Answer a few questions. Get a full PRD to build your app.

Got an app idea in your head, but no tech words, no developer, and no idea where to start? This skill turns that idea into a clear, screen by screen PRD, a Product Requirements Document, that any builder, or any AI builder, can follow without guessing, and without rebuilding it later.

For non technical founders: no tech words needed. Answer simple questions in plain words, and get a plan you can hand to a developer and say, build this, exactly this.

For developers and technical users: a structured PRD, with product summary, user roles and permissions, goals and non goals, screen by screen specs, business rules and logic, data and content, success criteria, scope, and a missing screens check, ready to brief Claude, Cursor, or any AI builder, or a human developer.

PRD means Product Requirements Document. In simple words, it is the full written plan for a product, before anyone builds it. It says what the product is, who it is for, what it must do, what it must not do, and what each screen must show and do. You do not need to know tech words, you just answer questions in plain words, and your AI agent writes the plan for you. This skill writes the plan. It does not build the app itself.

This skill does two jobs, in order. First, it asks the owner questions, one at a time, and writes down only confirmed answers. Then, it writes the full PRD as a draft for the owner to review. It never builds the app, it never publishes anything live, and it never invents facts, screens, prices, users, or rules.

Your AI agent is the worker here. The owner is the judge. Nothing is final until the owner approves the draft.

## When to use this skill

Use it when the user asks to:
- Write a PRD for a new app or website
- Plan a product before building it
- Turn a rough idea into a screen by screen plan
- Check a filled PRD for missing screens or rules before a build starts

Do not use it to build the app, write code, or publish anything. This skill only writes the plan.

## What you need first

Ask the user, one question at a time. Do not ask all questions in one long list. Ask one, wait for the answer, write it down, then ask the next. If the user does not know an answer, mark it as "Not decided yet", and keep going. Never guess an answer for the user.

Ask these questions, in this order:

1. What is the product, in one short sentence?
2. Who is it for, in plain words?
3. What problem does it solve for them?
4. What must the product do, in order of importance?
5. What must the product NOT do?
6. How will the user sign in, if at all?
7. What are the main screens, in the order the user sees them?
8. What happens on each screen, step by step?
9. What are the business rules, for example prices, limits, approvals, or who can see what?
10. What does success look like, in simple words, after the first version is used?
11. What is out of scope for the first version, and can wait for later?

If the user gives a short answer, ask one short follow up question to make it clear, then move on. Do not keep asking the same question in different words.

## Step 1: Ask and record

After each answer, record it in a simple list, with the question and the confirmed answer. Mark any answer that is not confirmed as "Not decided yet" or "Needs owner confirmation".

Rules for this step:
- Use only what the user actually said. Never add a feature, screen, price, or rule the user did not say.
- If a number is given, write it exactly as the user gave it. Never round it, change it, or invent a similar number.
- If the user says a feature is for later, write it under "Later, not in version 1", not in the main plan.
- Keep language simple, short, and plain, so a weak English reader can follow it.

## Step 2: Write the full PRD draft

After the questions, write the PRD as a draft file, clearly labelled "DRAFT - NOT LIVE - Owner approval needed" at the top. Do not build anything from it until the owner approves it.

Write the PRD in this order:

### 1. Product summary
- One short paragraph: what the product is, who it is for, and what problem it solves.
- Use only confirmed answers from Step 1.

### 2. Users
- List each type of user, in plain words, for example owner, customer, admin.
- For each user, write one line: what they can do, and what they cannot do.

### 3. Goals and non goals
- Goals: what version 1 must achieve, in simple words.
- Non goals: what version 1 must NOT do, and what is for later.

### 4. Screens, screen by screen
For each screen, write:
- Screen name
- Purpose, in one sentence
- What the user sees on the screen, in a short list
- What the user can do on the screen, step by step
- What happens after each action, in plain words
- What the screen must NOT show or do

Use the screens the user named, in the order the user sees them. Do not add a screen the user did not name, unless you mark it clearly as "Suggested, not confirmed, needs owner approval".

### 5. Business rules
- List each rule separately, with a number.
- For each rule, write: what the rule is, when it applies, and what happens if the rule is broken.
- Examples, only if the user gave them: prices, limits, approval steps, who can see what, what happens on an error.
- If a rule is not confirmed, mark it "Needs owner confirmation" and leave the detail blank, never guess it.

### 6. Data and content
- List what information the product needs, for example name, phone, email, order, price.
- For each item, write: is it required or optional, and who can see it.
- Never invent personal data, prices, or content the owner did not give.

### 7. Success check
- Write how the owner will know version 1 works, in simple words.
- Use only the success answer from Step 1.

### 8. Out of scope
- List everything that is for later, not in version 1.

## Step 3: Missing screens check

After writing the PRD draft, run this check, before giving it to the owner. This check is part of the skill, not an extra step.

Check for:
1. Is there a first screen, where the user starts?
2. Is there a sign in or sign up screen, if the product needs one?
3. Is there a main screen, home, or dashboard, where the user does the main job?
4. Is there a screen for each main action the user named?
5. Is there a success screen, or a clear message, after an important action?
6. Is there an error or empty screen, for when something goes wrong or there is nothing to show?
7. Is there a settings, profile, or help screen, if the user named one?
8. Does every screen in the plan have a purpose, a list of what the user sees, and a list of what the user can do?
9. Does every business rule have a screen where it is used, or is it a rule with no screen?
10. Is anything in the goals list missing a screen to do it?

Give the owner a short missing screens report, with three lists:
- Complete: screens that are fully described.
- Missing: screens that are needed but not in the draft, with a short note why they are needed.
- Not confirmed: screens or rules that need the owner's answer before they can be written.

Do not add a missing screen to the PRD by yourself. List it in the report, and ask the owner to approve it first.

## Output format

Give the owner this report, in this order:

1. Answers recorded
   - List each question, with the confirmed answer, or "Not decided yet".

2. PRD draft created
   - Name the draft file, and what it contains.
   - State clearly: "This draft is not live. Nothing has been built. Approve the draft first, then it can be used to brief a builder."

3. Missing screens report
   - Complete, Missing, and Not confirmed lists, as above.

4. Next steps for the owner
   - Approve, change, or reject each part of the draft.
   - Answer the "Not decided yet" questions.
   - Tell the agent which missing screens to add, and which to leave out.

## Hard rules

- Never invent a product, user, screen, feature, price, rule, or fact.
- Never add a screen or rule the user did not name, unless you mark it clearly as "Suggested, not confirmed".
- Never build the app, write code, or publish anything from the PRD without a separate, explicit owner approval to build.
- Never give a PRD a Pass without a missing screens check.
- If a fact is unconfirmed, mark it "Needs owner confirmation" and leave it blank in the draft, never guess it.
- Keep language simple, short, and plain. Avoid jargon, unless the owner asks for technical detail.
- A PRD is a plan, not a promise that the product will succeed, be used, or make money. Say that clearly if the owner asks.
