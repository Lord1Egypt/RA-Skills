---
name: postemi-templates
description: Postemi's library of ready post templates and hooks, the same ones the Postemi composer offers under Templates. Everyday posts, product launches, LinkedIn post types, X formats, conversation starters and more than 100 hooks (stories, contrarian takes, how-to, lists, books, habits, questions), each with [placeholders] to fill. Use when the user wants a quick draft of a common post type, a hook or opening line, a post idea for a goal (launch, engagement, teaching, story), or asks for templates.
---

# Postemi templates and hooks

The templates in [reference/](./reference/index.md) are generated from the
Postemi app, so they match what the user sees in the composer's Templates
column. Each has a title, a line on when to use it, and a body with
[placeholders] in square brackets.

Pair with `postemi-writing` (how to make the filled template good) and the
main `postemi` skill (how to preview and schedule it).

## Files

- [reference/index.md](./reference/index.md): every group and every template
  in one table (id, title, network, when to use it). Read this first, then
  open only the group file you need.
- Group files, with the full bodies:
  - [everyday.md](./reference/everyday.md): launch, behind the scenes, tip,
    roundup, customer story, event, question, milestone.
  - [launch.md](./reference/launch.md): announcing and explaining what the
    user builds.
  - [linkedin.md](./reference/linkedin.md): 30 LinkedIn post types in six
    sections (building in public, founder story, industry, team, teaching,
    conversation).
  - [x.md](./reference/x.md): short X formats.
  - Hooks, by what the post does:
    [hook-stories.md](./reference/hook-stories.md) (lessons and stories),
    [hook-contrarian.md](./reference/hook-contrarian.md) (contrarian takes),
    [hook-how-to.md](./reference/hook-how-to.md) (frameworks and how-to),
    [hook-lists.md](./reference/hook-lists.md) (lists and tools),
    [hook-learning.md](./reference/hook-learning.md) (books and learning),
    [hook-growth.md](./reference/hook-growth.md) (habits and growth),
    [hook-talk.md](./reference/hook-talk.md) (problems and questions).
  - [engagement.md](./reference/engagement.md): questions, polls and prompts
    that get replies.

## Pick a template

Start from the user's goal, then the network:

| Goal | Look in |
|---|---|
| Announce a product, feature or event | `launch.md`, `everyday.md` (`launch`, `eventReminder`) |
| Build trust as a founder or expert | `linkedin.md` (founder story, building in public), `hook-stories.md` |
| Teach something useful | `hook-how-to.md`, `everyday.md` (`quickTip`), `linkedin.md` (teach) |
| Start a debate, stand out | `hook-contrarian.md`, `linkedin.md` (`liHotTake`), `x.md` |
| Get comments and replies | `engagement.md`, `hook-talk.md` |
| Share tools, books, resources | `hook-lists.md`, `hook-learning.md` |
| Motivate, habits, personal growth | `hook-growth.md` |
| Show the team and culture | `linkedin.md` (team), `everyday.md` (`behindScenes`) |
| Social proof | `everyday.md` (`customerStory`, `milestone`) |

Network fit:

- Ids starting with `li` were written for LinkedIn and ids starting with `x`
  for X; the index says so in its Network column. The rest fit anywhere.
- A LinkedIn template on X: shorten it to the hook and one or two lines, or
  turn it into a thread (one point per entry). Check the account's limit.
- An X template on LinkedIn: add the context and a story; the hook must sit
  in the first two or three lines.
- For Instagram, TikTok and YouTube the template becomes the caption; the
  picture or video still carries the post.
- Remove any link from text going to X (Postemi strips links from X posts).

Offer two or three templates that fit and let the user choose, or pick one
and say why in a sentence.

## Fill it in

1. Ask the user for what the placeholders need, in one short message: the
   facts, the numbers, the story. Never invent them. A template with made-up
   details is worse than no post.
2. Replace every `[placeholder]`. Remove a line whose placeholder the user
   cannot fill, rather than leaving it vague.
3. Number placeholders (`[number]`) must be true numbers, and a list must
   have as many items as its hook promises.
4. Rewrite in the user's voice. The template is a skeleton, not a script:
   change words, order and length freely. Keep the shape that makes it work
   (the hook, the turn, the takeaway).
5. Hooks are openings: a hook template gives the first lines; write the rest
   with `postemi-writing` (keep the promise of the hook, lead with the best
   part, end with one takeaway or question).
6. Run the check in `postemi-writing` (section 7), then preview and schedule
   with the main `postemi` skill.

## Example

User: "I want to post on LinkedIn that we finally shipped dark mode."

1. Goal: announce a feature; network: LinkedIn. Candidates: `liFeature`,
   `liBuiltWrong` (if customer feedback changed the plan).
2. `liFeature` body: "We just shipped [feature]. It took us [time], longer than
   we planned. The reason: [...]".
3. Ask: how long did it take, what was harder than expected, what can people
   do now, one lesson.
4. Fill, rewrite in the user's voice, check, `preview_post` (or show the text
   in the CLI flow), schedule on the user's yes.

## Keeping this in sync

These files are generated. In the agent repository:
`pnpm sync:templates <path to the app's templates folder>`, then
`pnpm sync:skills`, then commit. Do not edit the reference files by hand.
