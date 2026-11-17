# The creative brief

## What this file is

**One spec, shared by every video scenario skill in this repo** —
`seedance-short-drama`, `seedance-anime-drama`, `seedance-ad-creative`,
`seedance-product-video`, `keyframe-animation`, `product-demo`, and any
scenario skill added later, `seedance-`-named or not. It is the rule
for what to ask the user **before** a prompt exists. Each scenario skill links
here and adds only its own question set; none of them restate what follows,
because four paraphrases of "ask once, recommend first, never default to the
AI" drift into four different rules.

Three shared files, three jobs, read in this order:

| File | Answers |
|---|---|
| **this file** | What do I ask the user, and when do I stop asking? |
| `prompt-structure.md` | Once the answers are in, how is the prompt built? |
| `approval-gate.md` | What must the user see, and say, before money moves? |

Read this **before writing the prompt**, and therefore before `--dry-run`.
Asking costs nothing and `--dry-run` needs no API key, so the whole brief
happens on the free side of the gate.

It lives in `ofox-video-core/references/` because that is the one skill every
scenario in this repo depends on. If you are reading a skill that links here
and the link missed, the rules below still apply either way, and there are two
reasons it can miss. The link is written as `../ofox-video-core/...`, which is
how skills.sh, ClawHub and `npx ofox-skills` name the directory; LobeHub
unpacks each skill as `ofoxai-skills-<name>`, so there the file is present
under a name the link doesn't use — the skill's own "Where the core skill
lives" section (called "Where the two core skills live" in a skill that uses
both) has the probe that finds it. Only if that probe comes back
empty was the skill really installed without `ofox-video-core`. Installing it
is the user's call, not yours — hand over the command rather than running it:
skills.sh is `npx skills add ofoxai/skills --skill ofox-video-core`, this
repo's wrapper is `npx ofox-skills ofox-video-core`, and on LobeHub or ClawHub
it is `ofox-video-core` from the same publisher. Ask for the one missing skill
rather than the whole repo, and give all three routes — naming one installer
tells a user of the other two to abandon theirs.

## The three tiers

Read the user's message and every attachment first. Then mark every axis of
the clip **settled** or **open**. Only open axes are ever asked about, and
only two of the three tiers can be open at all.

| Tier | What belongs here | What to do |
|---|---|---|
| **must-ask** | Without it the prompt cannot be written, or would be written wrong, and nothing in the input settles it. Typically: which part of a larger request to render; whether an asset the request implies actually exists; any axis that a later step will freeze irreversibly. | Ask. **Never** offer "Let the AI decide" on these — the AI cannot pick which of several things the user meant, and cannot conjure a file that does not exist. |
| **ask-if-open** | Several answers are all valid, taste decides, and the picture changes visibly. | Ask when the input leaves it open; skip when the input settles it. Each of these carries a "Let the AI decide" option, last. |
| **never-ask** | A sane default exists, or the choice moves the price rather than the picture. | Do not ask. Fill the default, and let it appear as a row in the cost table — **the table is where the user changes it.** |

The never-ask tier is not a shortcut past consent. Those values are still
approved, in the cost table, alongside the price they cause. A question about
one of them is a question the table already asks better: two resolutions are
two rows with two prices, which is more informative than an `AskUserQuestion`
with two labels and no numbers.

## One round — two, for a published deliverable

If any axis is open, ask **once** with `AskUserQuestion`: at most **four**
questions, usually two or three. The axes are independent of each other, so
they belong in the same call — do not drip one question per message.

**One** follow-up call is allowed, and only when an answer opened a branch
that did not exist before it was given. After that, no more questions: write
the prompt and `--dry-run` it.

**A second round of up to four questions is allowed — not "no more
questions" — when the clip is going out under the user's name rather than
being previewed once and set aside**: a page asset, a published post, a
client deliverable, or anything the user describes that way ("for the
site", "to publish", "for the gallery"). The second round is not a second
helping of taste questions on top of the first; it is reserved for **how the
seconds are spent** — see "Pacing questions belong in round two" below.
Everything else about a round still applies to it: independent axes in one
call, a recommendation first, "Let the AI decide" last. A single-shot
preview, an internal draft, or a small request stays at one round; when it
is unclear which tier applies, default to one round and let a scenario skill
name the published tier explicitly rather than assume it.

If four slots are not enough, in either round: **must-ask first**, then the
axis that changes the picture most, then the rest. Whatever does not fit
takes its default and becomes a row in the cost table.

### Pacing questions belong in round two

Five axes decide how a clip's *seconds* are spent, not what appears in them,
and until now every scenario skill left all five to the agent's own
judgement by default — which is how a 30-second clip spent close to a
quarter of its runtime recovering from its own climax and mirroring its
opening shot, while the six shots in between carried the entire fight on an
even, undifferentiated allowance (job
`4e5c9581-d462-443b-9663-b1aa6d72f527`, 2026-09-03; a scenario skill's own
account of it is in its `SKILL.md`). These axes are **ask-if-open**, each
carrying a "Let the AI decide" option like any other taste axis, and when a
brief has reached round two they belong there rather than in round one —
round one settles what is in the picture, round two settles how long each
piece of it holds the screen.

| Axis | What it changes | Ask when |
|---|---|---|
| **Duration split** | how many seconds go to the setup, to the core (the fight, the exchange, the reveal — whatever the beat is actually about), and to the close | the clip has a clear "main event" whose share of the runtime is not obvious from the request |
| **Ending length** | whether the close is where the beat's payoff lands (a final line, a landing action) or a brief settle after the payoff already happened earlier in the clip | the register leaves this open; each scenario skill's own version of this axis says which default applies to which genre |
| **Slow motion / freeze frame** | whether either appears at all, and how much of the duration budget they are allowed to spend | the request implies a climactic hit, reveal or beat where either is a plausible choice |
| **Density of the standout segment** | whether the best beat gets shorter, more numerous shots than the segments around it, or the same even spacing as the rest of the clip | the clip runs 20s or longer and has an action, spectacle or comic beat that is meant to be the reason to watch it |
| **Hard-cut share** | roughly what fraction of the boundaries are true cuts rather than in-camera transitions — a timeline weighted toward continuous transitions can soften even an explicitly written hard cut (see the two 30-second Ofox runs under "Several shots in one job" in `prompt-structure.md`) | more than three boundaries are planned and a definite cutting rhythm matters to the beat |

A scenario skill's own question table carries the exact wording, the
recommended option and the rest of the options for these axes — this file
only fixes where they sit and when the second round opens. Not every
scenario needs all five; add the ones the scenario's axis actually applies
to.

## Zero questions is legitimate and common

A request that names the format, the platform, the look and the content has
settled every axis. Write the prompt. **Do not invent a question to look
collaborative** — an unnecessary question costs the user a round trip and
teaches them that the brief is theatre.

## The shape of a question

- `header`: 12 characters or fewer, the axis name.
- `question`: one sentence saying **what this choice changes**.
- `options`: two or three concrete choices, then **"Let the AI decide"** last.
- Option 1 is the recommendation. Its label ends `(recommended)`, and its
  description says **why** — a gallery case number or a scenario convention,
  not "it's the default".
- Options 2 and 3 must be **visibly different pictures**, not synonyms.
  "Cinematic / premium / high-end" is one option wearing three labels, and
  the user cannot choose between labels.
- Each description is one or two sentences: the picture it produces, and the
  trade-off (slower, pricier, riskier, less faithful).
- Do **not** add an "Other" option. The tool supplies free-text entry itself,
  and a free-text answer is a legitimate answer — take it as stated.

## "Let the AI decide" — three rules

1. **Always last, never pre-selected, never the default.** The recommendation
   is option 1; the delegation is the final option. Silence is not delegation
   either — an unanswered call is an unanswered call.
2. **It resolves to a concrete value.** When it is chosen, pick one and write
   it into the recap marked `(AI's pick)`. Never `auto`, never `default`,
   never "the model will figure it out". The user approves a specific value in
   the cost table; `approval-gate.md` requires the same of model ids.
3. **"You decide" / "just do it" / "whatever looks good" delegates every
   ask-if-open axis at once — and leaves must-ask untouched.** A missing asset
   is still a missing asset. When the user delegates in the same breath as the
   request, ask only the must-ask items, in one call, and say that the rest
   were taken as delegated.

## Skip table — settle these without asking

An axis is **settled**, and is not asked, when the input decides it. Record
inferred values in the recap as `(inferred from "…")` so the user can overrule
them at the gate.

| Signal in the input | Axis | Value |
|---|---|---|
| An explicit value for that axis, anywhere in the request | that axis | as stated, including a free-text answer to an earlier question |
| TikTok, Reels, Shorts, Douyin, Kuaishou, "for my phone feed", "vertical" | aspect | `9:16` |
| YouTube, a web page hero, a landing page, Bilibili landscape, "landscape", "widescreen" | aspect | `16:9` |
| Amazon, Etsy, Shopify, a marketplace tile, a main listing image, "square" | aspect | `1:1` |
| An image attached to the request, or a path given | asset question | settled — **do not ask whether an asset exists** after one arrived; ask at most which route it takes |
| A second request for the same material in the same session | every axis answered last round | reuse; re-ask only what the new message changes |

Scenario-specific inference rows — the words that map to a style, a tone, a
motion, a spoken language — live in each scenario skill's own brief section,
because the vocabulary differs per scenario.

## Every answer lands somewhere

Every answer must be findable afterwards in the prompt text or in a flag.
Each scenario skill carries its own answer-to-prompt table for this.

**An answer that cannot be pointed at was a question that should not have been
asked.** This is the test to apply while drafting the question set, not after:
if you cannot name the sentence or the flag an answer would change, delete
the question and let the default stand.

## Order, with the approval gate

```
read input → fill the brief → [open axes] round one (up to 4 questions)
→ [an answer opened a branch] one follow-up
→ [a published deliverable, open pacing axes] round two (up to 4 questions)
→ write the prompt → --dry-run
→ one message: brief recap (AI's picks and inferred values marked) + full prompt + cost table
→ wait for an explicit yes → generate → report the real bill
```

The recap and the cost table go in **one message**, so the user sees what they
chose, what was chosen for them, and what it costs, before saying yes. The
recap block's format:

- One line per axis, in the order the questions were asked.
- Each line tagged with where the value came from: `(your choice)`,
  `(inferred from "…")`, or `(AI's pick)`.
- A final line listing the never-ask defaults, noting that they are rows in
  the table below.

Then the full prompt, then the table `approval-gate.md` specifies.

**Changing a row after that is a new table and a new yes — it does not reopen
the brief.** A yes to the table is the only approval to spend. Choosing an
option in the brief is not one, and neither is answering a follow-up.

## Without AskUserQuestion

`AskUserQuestion` is unavailable in some agent runtimes, and unavailable to
sub-agents even where the main session has it. When it is missing, put the
same questions in **one message** as a numbered list, each with lettered
options, the recommendation marked `(recommended)` and "Let the AI decide"
last. Same limits: at most four questions, one round, one optional follow-up.
Then continue with the same flow.

## Anti-patterns

1. **More than four questions in one round, or a second round that neither
   an opened branch nor the published-deliverable tier justifies.** A
   follow-up is for a branch an answer opened; a second round is for the
   pacing axes on a published deliverable — neither is a place for questions
   that simply did not fit in the first call.
2. **Asking what the input already settled.** The platform was named and you
   asked for the ratio; an asset was attached and you asked whether one
   exists; the request stated a value and you offered three.
3. **Asking and then not using the answer.** The user chose one thing and the
   prompt says another, or the answer appears nowhere at all.
4. **"Let the AI decide" placed first, pre-selected, or applied silently** —
   including treating no reply as delegation.
5. **Writing `auto` or `default` in the recap** instead of the value that was
   actually picked.
6. **Open-ended taste questions** — "what style do you want?", "any aesthetic
   preferences?" — instead of two or three concrete pictures and a delegation.
   Users cannot describe a look; they can choose between looks.
7. **A price question dressed as a taste question.** Two resolutions are two
   rows in the cost table, not an `AskUserQuestion`.
8. **Treating an answer as permission to spend.** Only an explicit yes to the
   cost table is; see `approval-gate.md`.
9. **Asking an axis that an earlier paid step has already frozen.** In a
   two-phase flow, anything the generated asset fixes — the frame shape most
   of all, because an attached image drives the clip's shape through
   `adaptive` (forced on `bytedance/seedance-2.5`, the default on other models
   that offer it) — must be asked before that asset is paid for. Asked
   afterwards, the only fix is paying again.
10. **Leaving a must-ask asset question until last.** Four questions about
    mood and camera, and only then discovering there is no usable asset,
    invalidates the answers already given: the whole prompt route changes.
    Assets first, taste second.
