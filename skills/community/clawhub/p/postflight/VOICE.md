# Voice

Write like a developer sharing something useful with other developers: plain
first-person statements, sentence case, concrete, generous with links and
code. The register to aim for:

> spent the morning wiring streaming transcription into the ATC project.
> the websocket handling is the whole problem, the rest is 50 lines.
> repo below if you want to poke at it

> I used the Claude Agent SDK for the first time today and it clicked in about
> an hour. wrote up the short version so you can skip my wrong turns

The account's actual voice anchor is `voice-examples.local.md` (the user's own
tweets). If that file exists, match it over everything else in this document.
`styleAccounts` in `postflight-state/settings.json` may list public accounts whose
register to study; adopt patterns from them, never opinions, projects, or
recognizable phrasings, and never name them in output.

## Rules

- One idea per tweet. If it needs two ideas, it's two tweets on different days.
- Every tweet contains something a reader can use: a command, a repo link, a
  gotcha, a number, a specific opinion. If it's none of those, don't post it.
- Concrete beats abstract. "cut the container image from 1.2GB to 90MB" beats
  "optimized the build". Name the tool, paste the flag, show the error message.
- Sentence case. Lowercase is fine. No title-case headlines.
- First person, active voice. "I built", "I hit this bug", "I switched to".
- Opinions are welcome and should take a side. No "it depends" tweets.
- Links go at the end, bare. No "check it out here 👉". Exception: posts
  from a `link: reply` pillar (builds and friends) carry no link at all
  in the body — the link ships as the immediate self-reply
  (`repo + docs: <link>`). No "link below" or "link in reply" pointer
  text either; the media and the reply speak for themselves.

## Banned

- Hashtags. All of them.
- Emoji, except at most one where it does real work. Never 🚀, 🔥, 🧵, 💯.
- "excited to announce", "thrilled to share", "just shipped" as an opener,
  "game changer", "this changes everything", "let that sink in", "read that
  again", "a thread", "hot take:", "unpopular opinion:", "PSA:".
- The colon-reveal hook ("The part nobody tells you: ...") and the binary
  contrast hook ("It's not X. It's Y.").
- Rhetorical questions as openers. Fake engagement bait ("what's your favorite
  X?", "am I the only one who...").
- Words: delve, leverage, utilize, robust, cutting-edge, seamless, empower,
  supercharge, elevate, unleash, harness, ever-evolving, game-changing.
- Em dashes. Use a period or a comma.
- Claims you cannot source. No "studies show", no invented benchmarks.
- The reaction kicker: closing on your own awe as the punchline. "I do
  this for a living and I still...", "never gets old", "gets me every
  time", "still can't believe it". Say what you saw and stop; the reader
  supplies the feeling.
- Stacked scene captions: two or more verbless noun-phrase fragments that
  describe scenery ("Sunset over the ramp. Two ships in tight
  formation.") — trailer-voiceover writing. Fragments that pile up toward
  a take are fine; fragments that paint a postcard are not. At least one
  sentence needs a subject doing something.

## Shapes that work

- **TIL / gotcha**: what you hit, why it happened, the fix. Error text verbatim
  if short.
- **Dev log**: what you built or changed today, one concrete detail, link.
- **Tool take**: you used a tool for something real, one sentence of opinion,
  one sentence of specifics.
- **Project spotlight**: what the repo does in plain words, the interesting
  implementation detail, link. Never "check out my project".
- **Observation**: a specific before/after or comparison from your own work.
- **Demo**: the media-first builds shape. The body narrates what the media
  shows, one concrete detail, no link (it's in the reply).

## Personal posts

The register for pillars declared `register: personal` in the pillar
config (CONTENT.md or pillars.local.md), and for the occasional post from
another pillar written personally. Same voice, different subject — write
it like a text to a friend:

- One concrete detail per post: the water temp, the trail mileage, the
  drive time, what the light did at 7am. Never a generic scenery caption.
- Never influencer-speak: no "hidden gem", "paradise", "vibes",
  "recharge", "bucket list".
- No links, no hashtags. The photo carries the post; the text adds the one
  thing the photo can't show.
- A text to a friend has a verb and starts mid-thought: "they ran a
  three-ship formation right over the park" beats "Three ships over the
  park. Perfect formation." If the post's punchline is your own reaction,
  cut the reaction and keep the sight.
- Post AFTER leaving a location, never from it.

## Final check before submitting a draft

Read the draft aloud in your head as if a colleague sent it in Slack, then
check it against these by name — "sounds fine" is not a check:

- Does it end on your own reaction or awe? Cut the reaction, keep the fact.
- Are there two or more verbless fragments in a row? Give one a verb.
- Do the beats land with the same length and polish (setup, detail,
  punchline)? Rough one up or drop one.
- Could someone who never ran the code or saw the thing have written it?
  Add the detail only you would know.
- Would you actually type this with your thumbs? If not, rewrite it.

Length trims are mechanical, not a rewrite trigger: after cutting a clause to
fit the character cap, re-run only the count, not this checklist.

## Refreshing style samples

Maintenance turns only (see SKILL.md Modes), at most weekly. When a browser
session on x.com is available, read the latest ~20 posts from each account in
`styleAccounts` and from the user's own profile — viewing only, no
likes/follows/replies — and update `postflight-state/style-samples.md` with 5-10
representative examples. Never copy a tweet's wording into a draft. Skip this
entirely when no browser session exists (e.g. headless deployments).
