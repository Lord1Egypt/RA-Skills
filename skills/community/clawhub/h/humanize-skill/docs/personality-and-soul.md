# Personality and soul: when the patterns are clean

This document is the missing layer between `docs/anti-ai-patterns.md` and `docs/voice-profile-deep.md`. The pattern catalog tells you what to remove. The voice profile tells you what rhythm to match. Neither, on its own, makes a piece of writing feel like a *person wrote it*. This document is about that third thing.

It borrows the spirit of `blader/humanizer`'s "PERSONALITY AND SOUL" section, which is right that pattern-removal is not enough. It does not borrow the idea that the skill should invent a personality when none is supplied. That is fake soul, and the skill rejects it. See `SKILL.md` Non-goals and `docs/anti-ai-patterns.md` "What this catalog is not".

## What "soul" actually means

When readers say a piece of writing "has soul", they mean the writer is *present* on the page. You can feel a person behind the words, with a specific mind, specific experience, and a specific take.

A piece of writing without soul reads as *constructed*. The words are correct. The structure is clean. The argument is technically sound. But the writer could be anyone. The reader cannot name the writer from the prose.

The two failure modes are:

- **No soul, no voice**: AI text that is also generic on the surface (promotional language, three-clause parallelism, vague attribution). The pattern catalog catches this.
- **No soul, voice present**: a piece of prose that has the user's rhythm and diction, but no real presence. The text is technically human-sounding but the writer is invisible. The pattern catalog does not catch this. The voice profile does not catch this. Soul is what catches this.

## Soul is not decoration

A common confusion: soul = personality quirks, a bit of humor, an exclamation mark, a colorful metaphor. This is decoration. Decoration can help, but it is not what makes a writer feel present. The presence comes from the *content of the thinking*, not from the surface.

The five sources of soul, in order of how much they move the needle:

### 1. Concrete experience

The strongest signal of a person. Specific numbers, names, places, dates, sensory detail, and a small story that the writer alone could tell.

- "I shipped the first version on a Saturday in March 2024, and the deployment broke the test environment for 90 minutes. I was the only one in the office. I had been awake for 20 hours."

This is impossible for AI to fake convincingly, because the details are too specific, too embodied, and too contextual. When the user supplies such a story, the rewrite *surfaces* it. When the user does not, the rewrite does not invent one — and a piece without a personal story is still allowed; it just leans on sources 2-5 instead.

### 2. Stated position

A piece of writing with a real position has soul. A piece of writing that hedges everything has none.

- Soul: "I think this is the right call, and I am willing to be wrong about it."
- No soul: "Some say this is right, others disagree, the answer is somewhere in between."

The position does not need to be aggressive. A quiet, considered position is also a position. The thing that matters is that the writer is on the page.

### 3. Visible reasoning

The reader can follow the argument because the writer shows the steps. "I started with X. I tried Y. The catch was Z. Here is what I think now."

Visible reasoning is a signature of a person thinking out loud. AI tends to compress reasoning to a conclusion. The rewrite *uncompresses* it, when the user has supplied the reasoning or when the position can be defended with a chain the user has not yet articulated.

### 4. Acknowledged contradiction

Real writers hold contradictions. AI tends to resolve them. "This is the right call, and it is also the call I would have made for the wrong reasons last year." Or: "I am not a fan of this approach in general, but for this specific case, it is what I would do."

When the user's draft has a contradiction, the rewrite keeps it. When the user's draft has resolved a tension that the user did not actually resolve, the rewrite puts the tension back.

### 5. Variation in tone and register

A real writer modulates. They are precise when precision matters and casual when it does not. They are dry in one paragraph and a little warmer in the next. They swear in the second paragraph of long posts. They allow themselves one bad joke in a technical piece.

A piece without variation feels like a template. A piece with the right variation feels like a person who is also paying attention to the moment.

## The difference between soul and fake personality

Fake personality is AI text that *performs* the markers of a person without having the substance. Common forms:

- **Performed enthusiasm**: "I'm thrilled to announce..." when the writer is not thrilled.
- **Performed humility**: "Of course, I could be wrong, but..." when the writer is certain.
- **Performed experience**: "I have seen this at three companies" when the writer has seen it at zero.
- **Performed humor**: a forced one-liner in a serious piece, or a "fun fact" sidebar in a technical report.
- **Performed stakes**: "This is the most important issue of our time" in a routine update.

Each of these is the AI's version of a human signal. The signal is a real thing (enthusiasm, humility, experience, humor, stakes), but the AI is producing the marker, not the underlying state. The reader feels the gap.

How to avoid fake personality in the rewrite:

- **Match the user's signals, not the surface forms.** The user is enthusiastic in their samples → the rewrite can be enthusiastic. The user is not → the rewrite should not be. The signal is in the *user*, not in a generic "writerly" style.
- **Do not invent a story to fit a beat.** If a paragraph calls for a personal anecdote and the user did not supply one, leave the paragraph without one. A paragraph without an anecdote is fine. A paragraph with a fake one is bad.
- **Do not over-perform the user's voice.** If the user swears in 1 of 10 paragraphs, the rewrite swears in 1 of 10. If the user uses "I think" in 3 of 10 sentences, the rewrite uses it in 3 of 10. Frequency matching matters.
- **When in doubt, write flat.** A flat paragraph is recoverable. A performed paragraph is not.

## Soul and the main workflow

The audience/persona pass aims the piece at a real reader. The pattern catalog (anti-ai-patterns) catches the surface. The voice profile (voice-profile-deep) catches the rhythm. The specificity pass (specificity-and-thought) catches the abstraction. The fact-check pass (fact-check) catches the unsupported claims. Soul is what is left to do after those passes.

In practice, the soul pass is small but decisive:

- After the main passes, read the rewrite aloud. Where does the writer disappear? Where do you feel the construction? Mark those spots.
- For each marked spot, ask: is there a concrete experience, a stated position, a visible reasoning chain, an acknowledged contradiction, or a tone variation that would put the writer back on the page? If yes, and if the user has supplied the material, put it in. If yes, but the user has not supplied it, leave a `note: soul-pass` flag in `notes.md` so the user can fill it in. If no, leave the paragraph alone.
- Re-read. If the writer is now present, the soul pass is done.

The soul pass is the last pass, and it is also the smallest in terms of edits. Most of the work was already done. The soul pass is the punctuation.

## How this differs from "fake personality" defaults

Some tools and prompts produce a default "friendly AI" voice: warm, helpful, a little informal, with a "let's dive in!" energy. That voice is not soul. It is a uniform. Many readers can feel the difference between a writer who happens to be friendly and a writer who has been defaulted to friendly.

The same applies to "brooding intellectual", "snarky expert", and "humble beginner" defaults. Each is a uniform. The skill does not default to any of them. The skill matches the *user's* actual voice, and looks for the soul that is already in the user's sample. When the sample is missing, the skill writes flat and flags the gap for the user to fill.

## What "rewrite, don't delete" means here

`blader/humanizer`'s "rewrite, don't delete" is right for the catalog level. When the pattern catalog flags a phrase, do not just delete the words; rewrite the surrounding sentence so the *idea* still lands. This is the same principle that runs through the humanize-skill workflow.

Applied at the soul level, "rewrite, don't delete" means: when the writer is missing from a paragraph, do not delete the paragraph. Rewrite it so the writer is in it. The fix is *not* to drop the paragraph. The fix is to find what the writer actually wanted to say and put *that* on the page, in the writer's voice, with whatever soul the sample carries.

## Tests for soul

Three tests, similar in shape to the tests in `docs/specificity-and-thought.md`:

- **The friend test**: if a friend read this paragraph, would they be able to say who wrote it? If yes, soul is present. If they would say "this could be from anyone", soul is missing.
- **The re-read test**: re-read the paragraph tomorrow. Does it still feel like a person, or does it flatten into a template on second read? Templates flatten. People do not.
- **The position test**: can you, as the reader, name the writer's actual position from the paragraph? If yes, soul is present. If you cannot tell where the writer stands, soul is missing.

These are subjective tests. The score is the writer's call, not a metric. But they are useful as a final pass before the rewrite is given back to the user.

## When the soul pass is not the right move

- **Reference, encyclopedic, and legal writing**: the writer is supposed to be invisible. Soul is not the goal. The pattern catalog and the fact-check pass are the work.
- **Marketing copy aimed at buyers**: the *product* is supposed to be visible, not the writer. The rewrite can have voice, but the soul is the brand's, not the writer's. Match the brand voice, not the user voice.
- **Short transactional messages**: a status update, a brief reply, a single-paragraph note. Soul adds noise. The rewrite should be plain.
- **When the user does not write often or did not supply a sample**: the soul pass is the smallest. The natural default voice carries the rewrite. Flag the gap, do not invent.

In all four cases, the soul pass is not skipped — it is just a check, not a write. Confirm that the writer's absence is correct for the surface, and move on.

## Summary

Soul is the writer being present. It comes from concrete experience, a stated position, visible reasoning, acknowledged contradiction, and tone variation. It does not come from performed enthusiasm, performed humility, performed experience, performed humor, or performed stakes.

The pattern catalog, the voice profile, the specificity pass, and the fact-check pass do most of the work. The soul pass is the last 5% that turns a clean rewrite into a piece of writing that feels like the user wrote it. It is also the easiest to fake, and the most damaging when faked. Be conservative. The user is the source of soul, not the skill.
