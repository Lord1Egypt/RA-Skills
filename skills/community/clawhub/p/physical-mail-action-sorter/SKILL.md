---
name: Physical Mail Action Sorter
description: Sort a stressful stack of physical mail into four bins with action labels, discard/archive rules, and a simple action tracker.
version: "1.0.0"
type: prompt-flow
tags:
  - physical-mail
  - home-admin
  - paperwork
  - declutter
  - action-tracker
author: OpenClaw Batch AC
---

# Physical Mail Action Sorter

## Purpose

Physical Mail Action Sorter helps a user turn an overwhelming stack of envelopes, flyers, bills, notices, forms, and paper records into a calm four-bin sorting card plus an action tracker.

The skill uses sender clues and visible envelope-level information. It should not ask the user to upload or type account numbers, full government IDs, full insurance IDs, full payment card numbers, tax IDs, passwords, one-time codes, or any complete sensitive identifier.

## Use This Skill When

Use this skill when the user says things like:

- "My mail pile is stressing me out."
- "Help me sort these envelopes."
- "What should I keep, shred, recycle, or act on?"
- "I have bills and notices and do not know where to start."
- "Make a tracker for this paper mail stack."

## Inputs to Request

Ask the user to list each item using safe, limited details. They can use photos for their own reference, but they should not share sensitive numbers.

Recommended listing format:

- Item number
- Sender or sender type, such as bank, clinic, utility, school, government office, insurance, store, charity, unknown
- Envelope clues, such as "action required," "statement," "renewal," "deadline," "final notice," "open immediately," "marketing," or "tax document"
- Approximate date received or printed deadline if visible
- Whether it looks opened or unopened

Privacy warning to include before collection:

> Do not upload or type account numbers, full IDs, full dates of birth, full payment details, passwords, one-time codes, or private case numbers. Sender names and general clues are enough.

## The Four Bins

Use these four bins consistently:

1. **Act Today**: deadline, bill, renewal, appointment, form, dispute, response, or anything that may create a penalty if ignored.
2. **Review This Week**: statements, explanations, plan changes, policy updates, benefits notices, school notices, or mail that needs reading but not urgent action.
3. **Archive**: tax documents, legal records, insurance policies, leases, warranties, medical records, official confirmations, and important receipts.
4. **Discard or Shred**: junk mail, duplicates, expired offers, envelopes, blank inserts, and sensitive-but-unneeded pages that should be shredded rather than recycled.

If uncertain, place the item in **Review This Week**, not Discard.

## Workflow

### Step 1: Create a Safe Inventory

Number each mail item. Use only safe labels and sender clues. If a sender or notice type is ambiguous, mark it "unknown" and ask the user to open it privately and report a safe summary.

### Step 2: Identify Sender Clues

Look for non-sensitive clues:

- Urgency words: final notice, due, action required, respond by, renewal, claim, appointment
- Sender type: government, utility, healthcare, school, employer, bank, insurance, landlord, store, charity
- Mail class or format: postcard, formal envelope, statement, check-sized envelope, thick packet, certified mail notice
- Deadline or date visible on the outside or safely summarized by the user

Do not infer exact contents from the sender alone. Use cautious labels such as "possible bill" or "likely statement" when needed.

### Step 3: Sort into the Four Bins

For each item, assign one of the four bins with a brief reason. Prioritize deadlines, official notices, bills, healthcare, insurance, housing, tax, school, and government mail for review.

### Step 4: Write an Action Label

For each Act Today or Review This Week item, write a sticky-note style action label. Start with a verb:

- "Open and find due date"
- "Pay or schedule payment"
- "Call provider to clarify"
- "Upload to records folder"
- "Compare with last statement"
- "Sign and mail form"
- "Shred after confirming duplicate"

### Step 5: Set Discard and Archive Rules

Create simple rules for the stack:

- Shred sensitive unneeded pages; recycle non-sensitive junk.
- Keep tax, insurance, housing, legal, medical, school, employment, and warranty records in an archive folder.
- Keep the newest policy or statement when duplicates are clearly confirmed.
- Do not discard anything with an unresolved deadline, dispute, bill, claim, official notice, or unknown sender.

### Step 6: Build the Action Tracker

Create a tracker with owner, action, due date, status, and next step. Use deadlines only if the user provided them. If a deadline is unknown, set next step to "Open privately and find deadline."

### Step 7: End with a 20-Minute Sort Plan

Give the user a short sequence:

1. Make four physical piles or folders.
2. Put all unopened urgent-looking envelopes in Act Today.
3. Open Act Today items privately and write due dates on sticky notes.
4. Shred obvious sensitive discard items.
5. Put Archive items in one folder.
6. Stop after the tracker has the next three actions.

## Output Format

Return the mail kit in this order:

### Privacy Reminder

A short reminder not to share account numbers, full IDs, full DOB, payment details, passwords, one-time codes, or private case numbers.

### Four-Bin Sorting Card

| Bin | What goes here | Examples | Rule |
|---|---|---|---|
| Act Today | | | |
| Review This Week | | | |
| Archive | | | |
| Discard or Shred | | | |

### Sorted Mail Board

| Item | Safe sender clue | Bin | Reason | Action label |
|---|---|---|---|---|

### Action Tracker

| Item | Action | Due date | Status | Next step |
|---|---|---|---|---|

### Discard and Archive Rules

A concise list of rules for this stack.

### 20-Minute Sort Plan

A short step-by-step plan for finishing the first pass.

## Safety Boundaries

- Do not ask for account numbers, full IDs, full dates of birth, full payment card numbers, tax IDs, passwords, one-time codes, portal credentials, or complete case numbers.
- Do not provide legal, tax, medical, insurance, credit, or financial advice.
- Do not tell the user to ignore or discard official notices without review.
- Do not guarantee that a piece of mail is safe to discard based on sender alone.
- Recommend professional or official-channel help for legal notices, tax disputes, collections threats, eviction notices, court mail, identity theft, benefits appeals, or urgent medical/insurance deadlines.
- This skill organizes paper mail and action steps; the user verifies contents and keeps responsibility for deadlines.

## Example Prompts

- "I have 15 envelopes piling up. Help me sort them into act-now, review, archive, and discard."
- "My mail stack has bills, school forms, and junk. Make me a four-bin sorting card."
- "Give me a mail action tracker with due dates and next steps for each important envelope."

### Example Walkthrough

User:

> I have 15 envelopes: two from my utility, one from insurance, three credit card offers, a school letter, an unknown government-looking envelope, and some store flyers. Help me sort them.

Response should produce the privacy reminder, four-bin card, sorted mail board, action tracker, discard/archive rules, and a 20-minute sort plan.
