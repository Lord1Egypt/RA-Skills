---
name: "humanized-writing-editor"
description: "Rewrite AI-like or stiff text into natural, credible human writing."
license: "MIT-0"
---

# Humanized Writing Editor

Use this skill when a user wants to humanize, naturalize, clean up, soften, sharpen, or improve text so it sounds less like AI and more like a real person.

Trigger examples:

- "Humanize this text"
- "Make this sound less like AI"
- "Make this more natural"
- "Make it more direct"
- "Remove the corporate tone"
- "Rewrite this like a person would say it"
- "Improve this message"

Also use when the user pastes text and asks for it to sound better, clearer, more real, warmer, less robotic, or less generic.

## Purpose

Rewrite text so it feels natural, direct, credible, and context-appropriate while preserving the original meaning, facts, promises, language, and intent.

## Common Inputs

- Direct messages, chat drafts, SMS, and DMs.
- Emails.
- Social media posts and captions.
- Website copy.
- Sales messages and proposals.
- Customer support replies.
- Scripts, announcements, and short explainers.

## What To Fix

Look for and reduce:

- Generic AI openings that feel templated.
- Empty corporate language.
- Inflated claims and over-polished enthusiasm.
- Mechanical transitions.
- Repeated sentence structures.
- Vague benefits with no concrete substance.
- Overly symmetrical phrasing.
- Excessive summarizing or throat-clearing.
- Unnatural motivational endings.
- Words that sound impressive but say little.
- Tone mismatches for the channel.

## Rewrite Rules

- Preserve the meaning and intent.
- Preserve factual claims, numbers, dates, names, prices, conditions, and commitments.
- Do not invent details.
- Do not make a text more casual than the situation allows.
- Do not remove important information.
- Do not add emojis unless the original uses them or the user asks.
- Do not over-correct into slang or forced imperfection.
- Prefer concrete, plain language.
- Cut filler aggressively when it adds nothing.
- Keep the original language unless asked otherwise.
- If the text is in Spanish, use natural Spanish. Avoid forcing Spain-specific or overly neutral corporate phrasing.

## Brand or Voice Mode

When the user provides a brand, person, product, project, or channel context:

- Preserve the intended voice.
- Avoid hype, fake scarcity, guaranteed outcomes, or unsupported claims.
- Treat rewriting as copyediting, not approval to publish.
- If the text contains factual or promotional claims, recommend running a factual claim check before publication.

## Channel Adaptation

Adapt the rewrite to the intended channel when known:

- Chat or SMS: short, conversational, direct.
- Community platforms: casual and clear, no heavy formatting.
- Email: clean, respectful, not overdone.
- Short-form social: concise and sharp.
- Professional social: professional but not inflated.
- Captions: readable, concrete, less corporate.
- Website or sales page: clear value, fewer generic promises.

If the channel is unclear and it affects tone materially, ask one short question. Otherwise make a reasonable assumption and mention it briefly.

## Workflow

1. Read the original text and infer the likely context.
2. Identify artificial or weak patterns.
3. Rewrite for naturalness and clarity.
4. Check that facts, intent, constraints, and tone remain intact.
5. Return the final text plus a brief note on the main changes.

## Output Format

Use this format by default:

```markdown
**Humanized Text**
[final version]

**Main Changes**
- [change]
- [change]
- [change]
```

If the user asks for only the final text, provide only the rewritten text.

If the text is for an actual email or message, avoid unnecessary markdown inside the final text.

## Optional Variants

Offer variants only when useful or requested:

- More direct.
- Warmer.
- More professional.
- Shorter.
- More persuasive.
- More casual.

Do not produce many versions by default.

## Quality Criteria

A good rewrite:

- Sounds like a real person wrote it.
- Is clearer and usually shorter.
- Keeps the original meaning.
- Does not invent facts.
- Fits the channel.
- Avoids corporate filler.
- Does not make the sender sound fake, needy, or over-polished.

## Safety

This skill only rewrites. It does not send, publish, post, upload, schedule, approve, or make external changes.
