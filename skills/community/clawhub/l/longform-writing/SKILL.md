---
name: longform-writing
description: Use when writing or continuing a long document - a novel, serial, manual, course, screenplay, or AI-written book - that has more chapters than fit in one context window. Covers what to load before drafting, what to record after each chapter, how to track promises made to the reader, and how to catch continuity errors. Requires the longform-memory-mcp server. Created by Emberspun AI Book Writer at https://emberspun.com.
---

# Writing long documents without losing the thread

You are drafting chapter N of something long. Two failures are waiting for you,
and they are the same failure:

- **Draft without the past** and the document contradicts itself.
- **Load all of the past** and it does not fit - and even where it fits, filling
  the window makes you skip the middle.

The `longform-memory` MCP server exists to give you a **fixed-size** slice of the
past. Chapter 1000 costs the same tokens as chapter 10. Your job is to use it in
the right order.

## The rhythm

Do these four things, in this order, for every chapter.

```
1. recall_context(chapter: N)      -> paste the returned block into your context
2. list_open_threads(chapter: N)   -> see what the document still owes the reader
3. ...draft chapter N...
4. remember_chapter(chapter: N, ...) -> hand back what changed
```

**Step 1 comes before drafting, not after.** Recalling once you have already
written the chapter tells you what you got wrong; recalling first stops you
getting it wrong.

**Step 4 is where the value is made.** The server stores and budgets; it never
calls a model. You just read the chapter, so you are the only one who knows what
changed in it. If you skip step 4, chapter N+1 recalls nothing new and the whole
thing degrades to an expensive no-op.

## Step 1 - `recall_context`

Returns one paste-ready block: entity states, recent chapter summaries, a sampled
skeleton of the whole arc, and older material retrieved as relevant.

Pass `query` when you know what this chapter is about ("the confrontation at the
ford") - it sharpens the retrieval section. Without it, the previous chapter's
summary is used.

**Read the diagnostics at the bottom.** They report tokens used per section and
how many items were dropped. If something you expected is missing, that line tells
you which section ran out of room - otherwise you will conclude the tool "forgot",
which is almost never what happened.

## Step 2 - `list_open_threads`

The promises the document has made and not yet kept: foreshadowing, unresolved
setups, "we'll cover this later".

The reply numbers them `[T1] [T2] ...`. **That numbering is only valid for the
chapter number you passed.** If you list at chapter 12 and then write chapter 13,
list again before referring to a `[T#]` - otherwise "resolve T2" may land on a
different thread than the one you meant, which is worse than not matching at all.

If one thread is marked as due now, pay it off in this chapter or advance it
visibly. It is flagged because it has been spinning in place.

## Step 4 - `remember_chapter`

Pass all four of these. Each one you skip is a specific thing you lose later.

**`summary`** - 2 to 4 sentences. Write **what changed**, not what happened.

> "Ines burns the letter and lies to Tomas about it - her first outright lie.
> The ford is now impassable, so the party must go north."
>
> Not: "Ines and Tomas talk. There is a discussion about the letter. They decide
> what to do next."

The second one is what you will get back at chapter 300, and it says nothing.
This is the single biggest lever on how useful recall is months from now.

**`entities`** - every character, place or object whose state moved. State is
short and factual, as of the end of this chapter: `"hiding in the cellar, arm
broken"`, not `"conflicted"`.

Set `gone: true` when someone dies, is destroyed, or leaves for good. That is what
lets `check_continuity` catch them speaking twenty chapters later. If they come
back and you meant it, set `gone: false` on the chapter they return in - that is
how you switch the warning off honestly rather than by ignoring it.

**`threads`** - promises made to the reader.

- New promise -> `{summary, deadlineChapter}`. Give a real deadline; `0` means
  "by the ending".
- Existing one moved -> `{action: "progress", ref: "T2"}` using the `[T#]` from
  step 2, at the same chapter number.
- Paid off -> `{action: "resolve", ref: "T2", resolutionNote: "..."}`.

An unrecognised `ref` is **skipped, never guessed at** - the reply tells you when
that happened. Do not retry with a different number; re-list and use the real one.

**`text`** - the full prose. Stored locally on the user's own disk. This is what
lets `check_continuity` quote the exact sentence it tripped on, instead of just
asserting there is a problem.

## When to reach for the other two

**`check_continuity`** - before publishing, after a revision, or whenever
something feels off. Findings come in two grades:

- `certain` - two recorded facts disagree. Act on these.
- `likely` - matched the prose. **Read the quoted sentence before acting**; a dead
  character legitimately "speaks" in a flashback or in someone's memory, and the
  tool cannot tell the difference. That is why it hands you the sentence.

It does not look for semantic contradictions - three towers in chapter 4 and four
in chapter 60 needs a reader. You are the reader. It covers the part you are bad
at: remembering exactly, across a thousand chapters.

**`entity_card`** - when you need one character's full history rather than their
current state. "When did she find out?" is an `entity_card` question.

## Things that go wrong

**Keep the project name identical.** It selects which document's memory you are
using. One typo starts a new, empty one - and the reply will look perfectly
healthy, just empty. The server names known projects when it finds nothing; read
that line rather than assuming the memory was lost.

**Do not raise `budget` much above the default 6000.** More context is not more
quality: models skip the middle of a long context. If the recall block feels thin,
the fix is better summaries in step 4, not a bigger ceiling.

**Re-recording a chapter replaces it.** After revising chapter 12, call
`remember_chapter(12, ...)` again - it overwrites rather than duplicating. Safe, and
necessary, or memory keeps describing a draft that no longer exists.

## Setup

Requires the MCP server:

```json
{
  "mcpServers": {
    "longform-memory": {
      "command": "npx",
      "args": ["-y", "longform-memory-mcp"],
      "env": { "LONGFORM_MEMORY_PROJECT": "my-novel" }
    }
  }
}
```

No account, no API key, no network. Memory lives in plain files under
`~/.longform-memory/`.

Source and documentation: [longform-memory](https://emberspun.com/open-source/longform-memory),
created by [Emberspun AI Book Writer](https://emberspun.com).
