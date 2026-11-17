---
name: youtube-script
description: Writes a YouTube video script in the chat, shaped to its genre (explainer, list, tutorial, review, story), with a hook, sections and one call to action, set out as what is SAID beside what is SEEN; only if the person wants footage does the SEE column go to Phantra as scenes. Writing it spends nothing. Use when someone asks for a YouTube or video script, or an outline. NOT for one scene's prompt (write-scene), scenes with no spoken script (storyboard) or the cover (thumbnails).
---

# YouTube script

A script is writing, done here in the chat. Nothing in this skill costs
credits, and no tool is needed until the person asks for footage. The studio
makes pictures, not narration: the voice is theirs to record.

## 1. Ask before writing

- **The topic and the one thing a viewer should leave with.**
- **Who it is for**, and what they already know.
- **The length** in minutes, and the **genre** (below).
- **What they know that a viewer does not**: their numbers, their story,
  their examples. These are the script; ask for them.

## 2. The shape, by genre

Every genre opens with a hook and ends with one call to action. The middle
differs:

| genre | the middle |
|---|---|
| explainer | the question, the plain answer, how it works in three parts, the common mistake |
| list | the items in rising order of interest, the strongest held for last |
| tutorial | the finished result, the steps in order, each with its one pitfall |
| review | the verdict, what was tested and how, what is good, what is not, who should buy |
| story | where it started, the turn, what it cost, what changed |
| commentary | the claim being answered, their position, the evidence, the strongest objection |

**The hook (the first 15 seconds)**: say what the video delivers and show
that it will, before any greeting, channel name or "in this video". One
sentence of promise, one of proof.

**Between sections**: a line that opens the next question, so there is a
reason to stay. **The end**: the payoff of the hook's promise, then ONE
thing to do next. Two asks are none.

## 3. Write it as SAY beside SEE

Two columns, a row per beat. SAY is the words, in their voice: short
sentences, written to be spoken. SEE is what is on screen: them to camera,
a screen recording, a product close-up, a title card.

| # | SAY | SEE |
|---|---|---|
| hook | "I ran this for a month. Here's what broke." | to camera, mid-gesture; cut to the broken part held up |
| 1 | ... | ... |

A spoken minute is roughly 150 words (the studio's advice, not a rule), so
say the word count beside the target length and cut to fit.

## 4. What is theirs, what is checked

Every fact, number, quote, test result and claim in SAY comes from the
person in this conversation. Never invent a statistic, a study, a quote or
an experience; where a line needs a fact you do not have, leave a marked
gap ("[your number here]") and ask. Never write a review of a thing they
have not used, and never write a line as if someone else said it.

## 5. If they want footage from the studio

Only on their ask. The SEE column becomes scenes; the SAY column stays a
voice they record.

- Each scene is 4 to 30 seconds of picture, rendered one timed shot at a
  time, and a rendered scene needs at least one of their photos. So the
  studio suits the inserts (a product close-up, a re-creation, an opener),
  not ten minutes of them talking.
- Pick the rows worth a scene with the person, then plan them together in
  storyboard (one `write_scene` per scene, filed in one project made with
  `create_project`) or write a single one with write-scene.
- Writing and saving a scene is free. Rendering is priced per scene by
  `quote` and runs only on their yes, through `approve`
  (price-and-render). Say how many scenes the plan is before quoting any.
- Finished clips are in `library`; `assemble_clips` joins them (no credits)
  and `share_link` hands over the file for their own editor, where the
  voice goes on. Scenes render in a vertical frame; `reformat` with
  `aspect` 16:9 makes a wide copy, padded or cropped, at no credit cost.

## 6. Keep what works

- `save_recipe` keeps their script format (the genre's order, their hook
  pattern, their sign-off) under a name, so the next script starts from it;
  `recipes` lists what they have saved.
- For the video's description or a caption, `score_caption` scores a draft
  against their own posted videos; with too little history it says so.

## Do not

- Never say the studio can narrate, add a voice, write subtitles onto the
  video or upload to YouTube; none of that is here.
- Never call a tool that spends while writing a script.
- Never pad to a length: cut the weakest section instead.
