---
name: postemi-writing
description: Write social media posts people stop for and read to the end, then schedule them with Postemi. Covers finding post ideas, hooks and headlines, opening lines, formatting and rhythm, threads, the writing rules of each network (X, LinkedIn, Instagram, Threads, Bluesky, Facebook, TikTok, YouTube and more) and a check before publishing. Use when the user asks to write, rewrite or improve a post, thread, caption, hook or headline, asks what to post about, or wants a post to reach more people.
---

# Postemi writing: posts that get read

This skill is about the words. Other Postemi skills sit next to it:

- `postemi` (the main skill): the tools or commands that preview, schedule and
  publish. Its rules win over anything here.
- `postemi-templates`: ready post templates and hooks with [placeholders],
  the same ones the Postemi composer shows. Start there when the user wants a
  quick draft of a known type (a launch, a tip, a poll).
- `postemi-growth` (optional, may not be installed): the plan over weeks: a
  niche, a 30-day test, cadence per network, reading the numbers,
  repurposing. If it is missing and the user wants a plan, tell them how to
  add it (`postemi skills add growth`, or the `postemi-growth` plugin); ask
  first, never install it yourself.

Reference files in this skill:

- [reference/headline-patterns.md](./reference/headline-patterns.md): 25 hook
  and headline patterns with examples.
- [reference/networks.md](./reference/networks.md): what works on each
  network, and what Postemi does there.

## Ground rules

1. Write in the user's voice, about the user's real experience. Ask for facts
   you do not have; never invent a number, a customer, a quote, a result or a
   credential. A made-up detail is the fastest way to lose a reader's trust.
2. A strong hook is fine only when the post pays it off. If the body cannot
   keep the promise, make the hook smaller, never the truth bigger.
3. Plain words, short sentences, one idea per post.
4. Show the user the draft before anything is scheduled (the main skill's
   preview step). The user decides; you suggest.

## 1. Find the idea

### The look-back test

People who "have nothing to write about" are usually writing for the wrong
reader. Ask the user three questions:

- What did you not know two years ago that you know now?
- What have you been through since then that you had not been through before?
- Where were you two years ago, and where are you today?

Every answer is a post. The reader is the person the user was two years ago:
someone a step or two behind, who wants to hear from someone who just did it,
not from a distant expert.

### The idea builder: topic, proof, angle

Build each idea from three choices.

**Topic, made narrow.** Start broad, then go down at least two levels, then
add who it is for and what they get:

- Broad: cooking.
- Narrower: cooking on weeknights.
- Narrower still: cooking dinner in 20 minutes after work.
- For whom, so that: for parents who get home at 6, so that the family eats
  together without takeaway every night.

The narrower the topic, the easier the post is to write and the quicker the
right reader knows it is for them.

**Proof: why should anyone listen?** Two kinds:

- Own proof: "This is what happened to me." Lived experience needs no title;
  say plainly that it is your experience.
- Borrowed proof: what someone with the experience says or showed: a study,
  a well-known practitioner, a customer, a book. Name the source honestly. On
  X, links are removed, so name it in words.

If the user has neither for a topic, pick another topic or borrow proof.

**Angle: which road do you take the reader down?**

| Angle | The post says | Example idea |
|---|---|---|
| How-to | Here is how to do it, step by step. | 5 steps to plan a week of dinners in 15 minutes |
| Analysis | Here is what the data or the trend shows, and why. | Why grocery bills rose more for small households this year |
| Inspiration | I did it, so you can too. | How I went from takeaway five nights a week to one |
| Human nature | Here is the hidden human reason behind it. | Why we buy vegetables we never cook |

Readers come back for the angle they liked. Try all four early; once the
numbers show which one the user's audience prefers, lean on it. Mixing is
fine later.

### A short interview when the user has no idea yet

Ask one question at a time, then offer three ideas, each with a hook:

1. What do you do, and for whom?
2. What question do people ask you most?
3. What did you get wrong at the start?
4. What do most people in your field believe that you disagree with?
5. What happened this week that taught you something?

For a whole month of ideas from one topic, use `postemi-growth` (30 angles)
if it is installed.

## 2. The hook

The first line (or the title, on YouTube and blogs) decides whether anyone
reads the rest. A good hook has these five qualities:

1. **Clear, not clever.** A pun makes a friend smile and a stranger scroll
   past. The reader must see at once what this is about and who it is for.
2. **A promise.** Not only "this is about X" but "after reading, you will
   have Y". No promise, no reason to give it 30 seconds.
3. **Specific.** Name the problem, the reader, or both. Vague reads as
   "not for me".
4. **A stance.** Lean one way. The right reader thinks "this is exactly my
   problem"; the wrong one thinks "not for me", and that is fine. A post for
   everyone is a post for no one.
5. **An open loop.** Say what they will get, hold back the answer. "Coffee
   makes you anxious" gives it away; "The one coffee habit behind my 3 pm
   anxiety" makes them read on.

### Build the hook from six parts

| Part | Question | Example |
|---|---|---|
| Number | How many things? | 4 |
| Kind | Tips, mistakes, lessons, reasons, steps? | mistakes |
| Topic | What exactly, two or three levels deep? | new runners make in their first month |
| Reader | Who is it for? (often implied by the topic) | new runners |
| Payoff | What does it get them, or save them from? | that lead to shin pain |
| More stakes | What else is at risk or to win? | missed races, quitting by spring |

Write the long version first, with every part:

> 4 mistakes new runners make in their first month that lead to shin pain,
> missed races and quitting by spring

Then cut to fit the network: drop extra stakes first, then adjectives.

> 4 first-month running mistakes that end in shin pain

Starting long and cutting is easier than trying to be short and sharp at once.

Ready patterns: [reference/headline-patterns.md](./reference/headline-patterns.md)
and the hook groups in the `postemi-templates` skill. Offer the user two or
three hooks for the same post and let them pick.

### Where the hook has to land

| Network | The hook is |
|---|---|
| X, Threads, Bluesky, Mastodon | the first line, and the first entry of a thread on its own |
| LinkedIn | the first two or three lines, before "see more" |
| Instagram | the first sentence of the caption (about 125 characters show), plus the image or the first second of the Reel |
| TikTok, Reels, Shorts | the first one to three seconds and the on-screen text |
| YouTube | the title (and the thumbnail the user makes) |
| Facebook | the first line; long posts fold after a few lines |
| WordPress, Ghost, Dev.to, Tumblr | the title |

## 3. The first sentence: six openers

Open with one sentence that does one of these:

1. **A bold statement.** "Most small shops do not need a website. They need a
   good photo on their map listing."
2. **A question that makes them think.** "Why do the best bakers in town
   never run out of bread at noon?"
3. **A contrary opinion.** "Posting every day is bad advice for most
   businesses."
4. **A moment in time.** "At 6:40 on a Monday, our only oven died with 200
   orders due."
5. **An honest admission.** "For three years I priced my work too low and
   called it being kind."
6. **A surprising fact or detail.** "Our slowest product sells best on rainy
   Tuesdays."

Facts in openers must be true and, where it matters, sourced.

## 4. Shape the post

**Outline before writing.** Four lines, then fill them in:

1. Working hook.
2. One line of proof (why the user can say this).
3. The main points (two to five).
4. The takeaway (the one thing to remember or do).

**Lead with the best part.** Do not make the reader wade through setup to
reach the useful bit. Every line should earn the next.

**Points that tell the story.** In a long post, a thread or a carousel, make
each main point a line that reads well on its own, so a skimmer gets the
whole story from the points alone. Use the points as section lines or as the
first line of each thread entry.

**The 1-3-1 rhythm.** Alternate a one-sentence paragraph with a paragraph of
about three sentences, then a single line again. Vary sentence length the same
way. It gives the reader a breath between ideas. On LinkedIn and Instagram,
read mostly on phones, keep most paragraphs to one or two sentences.

**End on purpose.** One of: a takeaway line, a question that is easy to
answer ("Which of these did you make?"), or one call to action. Never three.

**Text plus a picture or a video** usually beats text alone. Use the user's
own photos and videos (Postemi uploads them; it does not generate images or
video). A screenshot, a photo of the work or a short clip is enough.

**Format.** Postemi post content is HTML: each line in `<p>`, plus `strong`,
`ul`/`li` and `h1` to `h3` (never `u` and `strong` together). Networks show
formatting differently; line breaks and short lists are safe everywhere. The
preview shows the result.

## 5. Formats

- **Short post:** one idea, one to five lines. The daily bread on X, Threads
  and Bluesky.
- **Long post:** a hook, three to seven short paragraphs or a list, a
  takeaway. Strong on LinkedIn and Facebook, and on X for accounts with a
  higher character limit (the limit comes from the account, never guess it).
- **Thread** (X, Threads, Bluesky): the first entry must work alone and make
  people open the rest. One point per entry. The last entry sums up and asks
  for a reply or a follow. Ask the user whether they want a thread or one long
  post. On X, every thread entry counts toward the account's monthly X post
  allowance in Postemi.
- **Carousel** (LinkedIn image carousel, Instagram multi-image): one point per
  slide, the hook on the first slide, the takeaway on the last. The user
  supplies the images.
- **Video caption** (TikTok, Reels, Shorts, YouTube): the caption supports
  the video; the hook lives in the first seconds of the video itself.
- **Post plus first comment** (LinkedIn, Facebook): put the main text in the
  post and a link or extra detail in the first comment. In Postemi, the
  entries after the first are comments on these networks.

## 6. Network by network

Short version; details in [reference/networks.md](./reference/networks.md).

- **X:** short and direct; one X channel per post; no links (Postemi removes
  them, so put the link in the bio or tell the user to post it on X
  themselves); the character limit depends on the account; threads and every
  entry count toward the monthly X allowance.
- **LinkedIn:** the hook before "see more", short paragraphs, a question at the
  end to draw comments; long text with an image, or an image carousel, does
  well. Personal profiles only today (company pages are coming soon).
- **Instagram:** the picture or Reel first, then a caption whose first sentence
  hooks; a clear call to action; a few relevant hashtags. Reels want 9:16.
- **Threads, Bluesky, Mastodon:** conversational, short; threads work.
- **Facebook:** a friendly, local voice; questions and photos; links are fine.
- **TikTok, YouTube:** the video carries it; write a caption and (YouTube) a
  title that make a clear promise. TikTok takes about 15 posts per account per
  day.
- **Blog channels (WordPress, Ghost, Dev.to, Tumblr; beta):** a home for the
  long version of the user's best posts, with a title.

Never offer a network Postemi does not support (the main skill has the list;
Pinterest, Google Business Profile and LinkedIn company pages are not
schedulable yet).

## 7. Check before publishing

Go through this list for every draft, then show the user:

1. The hook is clear, specific, promises something and leaves a question open.
2. The body keeps the promise of the hook.
3. The best part comes first; nothing is padding.
4. Every fact, number and quote is true and came from the user or a named
   source.
5. One idea, one call to action at most.
6. Short paragraphs; the 1-3-1 rhythm; it reads well on a phone.
7. Every [placeholder] from a template is filled or removed.
8. It fits the account's character limit (from the schema, not from memory).
9. Network rules: no link in X posts; the LinkedIn hook sits above "see more";
   media where the network needs it (Instagram, TikTok, YouTube).
10. It sounds like the user, not like an advert. Read it aloud.
11. Hashtags, if any: few and relevant. Emojis, if any: where the user would
    use them.

## 8. From draft to scheduled, with Postemi

The workflow is always: **draft, preview, confirm, schedule.** The exact
calls are in the main `postemi` skill; in short:

Use whichever your client has. If the Postemi MCP tools are connected, use
them and never install the CLI; the CLI is for agents with a terminal.

With the Postemi MCP tools (Claude, ChatGPT, Cursor, Grok and other chat
clients):

1. `get_workspace_context` for the clock and the user's timezone.
2. `list_integrations`; pick channels by id; say the `@handle` back.
3. `get_integration_schema` for each channel: the real character limit and
   the required settings. Write within them.
4. `preview_post` with one `socialPost` entry per channel (each with its own
   text, so every network gets its own version) and show the result.
5. After the user says yes: `create_post` with the same payload and a new
   `idempotencyKey`. `type: "draft"` saves without scheduling.

With the `postemi` CLI (coding agents with a terminal):

1. `postemi auth:status`, then `postemi integrations:list`.
2. `postemi integrations:settings <id>` for the limit and the settings.
3. Show the user the text per channel and the local time; wait for a yes.
4. `postemi posts:create ... -t draft` to save, or with `-s "<date>"
   --timezone <IANA>` to schedule; `--json` for different text per channel.
   `postemi posts:find-slot <id>` suggests the next free slot.

After it goes out, the numbers tell you which hooks and angles work: see
`postemi-growth` (optional).
