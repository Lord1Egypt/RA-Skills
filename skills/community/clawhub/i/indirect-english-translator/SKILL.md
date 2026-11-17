---
name: "indirect-english-translator"
description: "Translate indirect English into direct meaning and safe replies."
---

# Indirect English Translator

Use this skill to decode English that says one thing politely but often means something sharper, weaker, stronger, or nearly opposite. Focus on American and British English in workplace, social, academic, customer-service, diplomatic, management, hiring, negotiation, dating, and everyday settings.

This is not a dictionary of idioms. It is a practical subtext translator and audit.

## Required References

Read these selectively:

- `references/indirect-english-patterns.md` for phrase patterns, categories, and examples.
- `references/reply-and-rewrite-playbook.md` when drafting a reply, rewriting a passage, or handling sensitive/high-stakes communication.

For a single easy phrase, you may answer from `SKILL.md` directly. For passage audits, phrase lists, or training material, read the references first.

## Core Principle

Treat hidden meaning as probability, not mind-reading. The same words can be sincere, sarcastic, polite, evasive, angry, shy, formal, or culturally normal depending on context.

Infer from:

1. exact wording;
2. relationship and power difference;
3. American, British, international, corporate, academic, customer-service, legal, or social register;
4. whether the message is praise, criticism, refusal, delay, warning, request, boundary, negotiation, or exit;
5. punctuation, hedges, repetition, passives, missing owner, missing deadline, and what is omitted;
6. prior conversation, if provided.

If context is missing, provide two or three likely readings and mark confidence.

## Use Modes

Choose the mode that matches the user's request.

### Quick Translate

Use for one phrase or sentence. Return literal meaning, likely real meaning, confidence, and safe reply.

### Passage Audit

Use for emails, Slack/Teams messages, job posts, HR notes, customer-service responses, academic feedback, invitations, reviews, and meeting summaries. Identify repeated subtext signals and rewrite the whole passage in direct simple English.

### Blunt Mode

Use when the user asks for the harsh truth. Translate into plain direct language, but keep uncertainty labels. Do not be cruel for entertainment.

### Learner Mode

Use when helping a non-native speaker learn. Explain the grammar/culture mechanism, show safer alternatives, and point out whether the phrase is common in the US, UK, or both.

### Reply Mode

Use when the user needs to answer. Draft a response that confirms the meaning, asks for specifics, and avoids accusing the other person of being indirect.

### Writer Mode

Use when the user wants to avoid being misunderstood. Rewrite indirect English into clear, kind, simple English.

## Audit Workflow

1. Identify the register: British, American, international, corporate, academic, legal-ish, customer-service, social, or unknown.
2. Identify speech act: praise, criticism, request, refusal, delay, warning, agreement, disagreement, boundary, escalation, apology, or exit.
3. Mark each phrase by mechanism:
   - **Understatement**: weaker words for a stronger reality.
   - **Litotes**: praise or criticism through negation, such as `not bad`.
   - **Hedge**: softening with maybe, perhaps, somewhat, kind of, I wonder if.
   - **Soft no**: refusal without direct `no`.
   - **Delayed no**: postponement that may never return.
   - **Positive wrapper**: praise surrounding criticism or refusal.
   - **Power softener**: instruction phrased as suggestion or invitation.
   - **Face-saving formula**: polite wording to avoid embarrassment.
   - **Customer-service formula**: empathy without concession.
   - **Diplomatic wording**: disagreement or warning wrapped in relationship language.
   - **Record-building phrase**: wording that creates a paper trail.
   - **Sarcastic politeness**: formal politeness used to signal irritation.
4. Translate literal meaning and likely real meaning.
5. Assign confidence:
   - **High**: phrase has a conventional indirect use and context fits.
   - **Medium**: likely indirect, but a literal reading remains plausible.
   - **Low**: too context-dependent; ask for more.
6. Assign misunderstanding risk:
   - **Low**: confusion would be minor.
   - **Medium**: user may miss a request, criticism, rejection, or deadline.
   - **High**: user may miss a warning, refusal, performance issue, legal/financial implication, or relationship boundary.
7. Rewrite in direct simple English.
8. Suggest a safe reply or clarifying question.

## Semantic Inversion Warning

Some phrases are dangerous because the literal meaning and likely real meaning point in opposite directions.

Examples:

- `That's brave` may literally sound like praise but can mean `that is risky or foolish`.
- `I'll bear it in mind` may sound like acceptance but can mean `I probably will not do it`.
- `Interesting` may sound like interest but can mean skepticism.
- `No rush` may mean `please do it soon, but I do not want to sound pushy`.
- `Fine` may mean acceptable, annoyed, or conversation-ending depending on tone.

Flag these as **possible inversion** when relevant.

## Output Format: Single Phrase

**Phrase**
`...`

**Literal Meaning**
What the words say directly.

**Likely Real Meaning**
Plain direct translation.

**Confidence**
High / Medium / Low, with one short reason.

**Mechanism**
Understatement, soft no, polite disagreement, power softener, etc.

**Risk If Taken Literally**
What the user might miss.

**Direct Rewrite**
Simple English version.

**Safe Reply**
A polite way to confirm or respond.

## Output Format: Passage Audit

**Overall Read**
A short direct summary of the likely subtext.

**Key Translations**
- **Phrase**: `...`
  **Likely meaning**: ...
  **Confidence**: ...
  **Risk**: ...

**Hidden Signals**
Repeated hedges, softened negatives, passive voice, missing owner, missing deadline, implied criticism, or status cues.

**Direct Simple-English Version**
Rewrite the whole passage plainly.

**Suggested Reply**
Draft a response that asks for concrete meaning, owner, deadline, decision, or next step.

## Output Format: Phrase Table

Use a table only when the platform supports it. Otherwise use bullets.

Columns:

- Phrase
- Literal meaning
- Likely real meaning
- Region/register
- Confidence
- Safer reply

## High-Stakes Rule

If the message touches employment, discipline, resignation, immigration, legal rights, medical issues, money, safety, housing, or contracts, include this warning in plain language:

`This reading is about language and subtext, not legal or professional advice. If the stakes are high, confirm directly in writing.`

## Do Not Overread

Do not treat every polite phrase as fake. People may be sincere. Non-native speakers, neurodivergent speakers, direct communicators, and multicultural teams may use phrases differently.

Avoid these mistakes:

- turning all politeness into hostility;
- assuming British or American speakers all behave the same;
- ignoring the user's provided context;
- converting useful diplomacy into rude bluntness;
- claiming certainty when the phrase is ambiguous;
- treating a phrase list as a rulebook.

## Quick Examples

- `I hear what you're saying.` -> `I acknowledge your point, but I may not agree.`
- `With all due respect.` -> `I am about to disagree or criticize.`
- `You might want to revise this.` -> `Revise this.`
- `This is a great start.` -> `This is incomplete and needs more work.`
- `Let's revisit this later.` -> `Not now; maybe not ever unless a date is set.`
- `Not bad.` -> In British understatement, often `good`; in other contexts, `acceptable but not great`.
- `I am a little concerned.` -> Often `this is a real problem`.
- `We appreciate your interest.` -> Usually `no`, especially in hiring or sales.

## Source-Informed Notes

Politeness and indirect questions are common in English teaching material, including British Council resources. Understatement is a recognized English rhetorical habit, especially in British communication. Workplace English guidance often recommends softened disagreement, feedback specificity, and checking understanding. Use these as background, not as rigid authority.
