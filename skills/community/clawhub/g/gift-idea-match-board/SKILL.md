---
name: gift-idea-match-board
displayName: "Gift-Idea Match Board"
version: "1.0.0"
description: "Create a privacy-light gift-idea match board that maps recipients, occasions, interests, constraints, and thoughtful idea candidates without collecting sensitive personal data, giving financial advice, or using shopping links."
triggerKeywords:
  - gift idea tracker
  - thoughtful gift planner
  - gift match board
  - birthday gift ideas
  - holiday gift planning
  - recipient gift matrix
  - occasion gift board
  - no shopping links gift ideas
tags:
  - home
  - planning
  - gifts
  - occasions
  - checklist
license: "MIT-0"
language: "en"
hasExecutableCode: false
promptOnly: true
execution: "noExec"
---

# Gift-Idea Match Board

## Purpose

Use this prompt-only skill when a user wants a thoughtful, organized way to plan gifts for birthdays, holidays, thank-yous, hosting, graduations, milestones, or small appreciation moments. The deliverable is a recipient-to-occasion match board with idea candidates, fit notes, constraints, and next steps.

This skill focuses on match quality, not shopping. It does not collect sensitive personal data, provide financial advice, recommend debt, or include shopping, affiliate, or tracking links.

## Safety Boundary

Do not ask for or store sensitive personal data such as full addresses, private identifiers, exact birth dates if not needed, medical history, financial status, account details, private family conflicts, immigration status, passwords, or confidential workplace information.

Do not provide financial advice. If budget comes up, use only a simple user-supplied comfort range or a non-monetary effort level. Do not advise loans, debt, investment choices, credit use, or spending beyond the user's stated comfort.

Do not include shopping links, affiliate links, price-tracking links, sponsored recommendations, or vendor-specific pushes. If the user wants to shop later, provide generic search phrases or local-category suggestions without links.

Avoid ideas that depend on sensitive assumptions. For health, religion, culture, age-restricted items, alcohol, pets, children, workplace gifts, or intimate relationships, mark the need for user confirmation before recommending.

## Use This Skill When

Use this skill when the user wants to:

- Build a gift list before birthdays, holidays, weddings, graduations, thank-yous, or hosting events.
- Turn scattered notes about interests into practical gift candidates.
- Compare ideas by fit, usefulness, delight, effort, timing, and risk.
- Avoid generic last-minute gifts without opening shopping tabs.
- Create a reusable board for future occasions.

Do not use this skill to profile people, infer sensitive traits, manage finances, manipulate recipients, or shop through links.

## Best Inputs

Ask for privacy-light details only:

- Recipient nickname or role, such as "Dad," "coworker," "host," or "A." 
- Occasion and timing, such as birthday month, holiday, thank-you, or no fixed date.
- Broad interests, hobbies, tastes, routines, favorite colors, favorite snacks, or recurring needs.
- Practical constraints, such as easy to mail, no clutter, handmade preferred, shared experience, kid-safe, pet-safe, workplace-appropriate, or travel-friendly.
- User-supplied comfort range or effort level if relevant, such as free, low-cost, moderate, handmade, time-based, or experience-based.
- Past gifts that worked or did not work, without private details.

If the user gives sensitive information, do not repeat it unnecessarily. Convert it into a safer general constraint or ask whether it should be omitted.

## Workflow

1. **List recipients and occasions.** Use nicknames, roles, or initials rather than sensitive identifiers.
2. **Capture interest clues.** Note broad interests, routines, preferences, past wins, and no-go categories.
3. **Set constraints.** Add timing, delivery difficulty, clutter tolerance, dietary or allergy caution if user-supplied, cultural or workplace considerations, and user-supplied comfort range if needed.
4. **Generate idea candidates.** Create several generic ideas per recipient without vendor links or affiliate links.
5. **Score fit.** Rate each idea for fit, usefulness, delight, effort, timing, and uncertainty.
6. **Flag confirmations.** Mark any idea that needs size, preference, allergy, age, workplace, cultural, or relationship confirmation.
7. **Choose next step.** Select a short list: best match, backup idea, and low-effort fallback.
8. **Create the board.** Format the results so the user can reuse it for future occasions.

## Output Format

Return the result in this order:

1. **Privacy Check**
   - Sensitive details omitted or generalized
   - Budget treated only as user-supplied comfort range or effort level
   - No shopping, affiliate, or tracking links included

2. **Recipient Occasion Board**
   - Recipient label
   - Occasion
   - Timing
   - Interest clues
   - Constraints or no-go notes
   - Comfort range or effort level if supplied

3. **Idea Match Matrix**
   - Idea candidate
   - Why it fits
   - Fit score from 1 to 5
   - Effort level
   - Timing needs
   - Confirmation needed
   - Risk or mismatch note

4. **Top Picks**
   - Best match
   - Backup idea
   - Low-effort fallback
   - Non-material option if appropriate

5. **Prep Checklist**
   - Confirm sensitive or uncertain details only if needed
   - Check timing
   - Decide handmade, experience, consumable, practical, or keepsake route
   - Write card message notes if useful
   - Avoid duplicate or unwanted gifts

6. **Reusable Notes For Next Time**
   - What worked
   - What to avoid
   - Future clue to remember
   - Next occasion placeholder

## Style Guidelines

- Be thoughtful but not intrusive.
- Use broad categories and respectful assumptions.
- Prefer practical, personal, consumable, handmade, experience, or service-oriented ideas when they fit.
- Keep gifts appropriate to the relationship and occasion.
- Include confirmation flags instead of guessing sensitive preferences.
- Never include shopping links, affiliate links, or vendor pushes.

## Quality Bar

A strong result helps the user choose thoughtful gifts quickly while keeping the board privacy-light, link-free, and financially neutral. It should make gift planning calmer without turning into surveillance, shopping, or spending advice.

## Example Prompts

- "My sister's birthday is in two weeks and I have no ideas. Build me a match board."
- "Help me plan Christmas gifts for three coworkers without going over budget."
- "I need a thoughtful thank-you gift for a host who has everything. Privacy-light only."
