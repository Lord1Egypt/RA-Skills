# Podwise Discover

Use this skill to expand the user's podcast world beyond their existing subscriptions. It combines what Podwise knows about the user — their followed shows, their interests, their level of engagement — with Podwise's trending and search tools to surface recommendations that feel personally relevant, not algorithmically generic.

## Goals

1. Verify the Podwise MCP connection.
2. Load `taste.md` to understand the user's current taste and gaps.
3. Identify what the user is looking for: new shows, new episodes, or both.
4. Use `get_popular_episodes` and `ask_podwise` to find candidates.
5. Filter out shows the user already follows.
6. Present a curated set of recommendations with clear reasoning for each.

## Step 1: Check the Environment

Call `get_me`. If the Podwise tools are unavailable or return an authentication error, stop and follow [../references/installation.md](../references/installation.md) before continuing.

## Step 2: Load the Listener Taste

Look for `taste.md` in the current working directory.

- If found, read the following fields silently:
  - **Core Interest Areas** — to drive `ask_podwise` queries and score relevance
  - **Shows to Prioritize** — to understand the style and depth the user enjoys
  - **Listening Style** — episode format and language preferences
  - **Output Preferences** — to shape how recommendations are presented
- If not found, stop and tell the user:

> "This skill works best with a taste profile. Please run `refine-taste` first so I can make recommendations based on your actual taste rather than generic popularity."

Proceed without a taste profile only if the user explicitly asks to continue anyway.

## Step 3: Clarify What the User Wants

If the user has not specified what kind of discovery they want, ask — all in one message:

1. **Type**: Are you looking for new *shows* to subscribe to, specific *episodes* to try, or both?
2. **Mood**: Are you in the mood to go deeper on something you already know, or explore something new to you entirely?
3. **Any constraints**: Any topics you want to avoid? Any format you dislike? (e.g. "no solo monologue shows", "only English", "under 30 minutes")

Use this information to shape the discovery in Step 4 — do not filter results based on Step 3 answers yet.

## Step 4: Gather Candidates

Use `get_popular_episodes` and `ask_podwise` as the primary discovery engines.

### Surface What's Trending

- `get_popular_episodes` with `limit: 20`.

Cross-reference popular episodes with the user's interest areas (from taste profile) or the topics they mentioned in Step 3. Keep any popular episode whose topic overlaps with their interests. These are the primary episode candidates.

### Ask for Adjacent Topics

Use `ask_podwise` to find podcast content on topics *adjacent* to what the user already knows — to expand rather than reinforce:

- `ask_podwise` with a question such as `"podcasts about {adjacent topic}"`.

`ask_podwise` counts against the user's Ask quota and can take up to 60 seconds — do not cancel early.

The answer includes cited source clips with episode seqs. Choose 1–2 adjacent topics by reasoning from the taste profile:
- If the user follows AI podcasts, an adjacent topic might be "cognitive science" or "the history of computing"
- If they follow investing podcasts, adjacent might be "economic history" or "behavioural psychology"
- If they follow fitness podcasts, adjacent might be "sleep science" or "nutrition research"

If no taste profile is loaded, base the adjacent topic query on the user's Step 3 answers about mood and interests.

### Optional: Targeted Search

If the user explicitly asked for shows or episodes about a specific topic, use search as a targeted lookup — not as a default discovery path:

- `search_podcasts` with `query: "{topic}"`.
- `search_episodes` with `query: "{topic}"`.

## Step 5: Filter and Score Candidates

Build the already-followed whitelist from two sources:

- `list_followed_podcasts` with `days: 30` — shows the user follows that published recently. **This only covers recently active shows, not the full follow list.**
- The **Subscribed Podcasts** section of `taste.md`, if loaded — use this to catch follows the tool missed.

Filter rules in order:

1. **Remove already-followed shows**: cross-reference every candidate podcast against the whitelist. Drop any show the user already follows. If `taste.md` is not loaded, note that the whitelist may be incomplete because `list_followed_podcasts` omits shows with no recent episodes.
2. **Remove Shows to Prioritize**: drop any show that appears in the user's **Shows to Prioritize** list — these are shows they already engage with regularly.
3. **Remove Shows to Deprioritize**: drop any show that appears in the user's **Shows to Deprioritize** list — these are shows the user has consciously deprioritised.
4. **Remove format mismatches**: if the user expressed a format preference in Step 3, drop episodes or shows that do not match (e.g. drop daily news shows if the user prefers long-form).
5. **Remove language mismatches**: drop content in languages the user did not indicate they listen to.
6. **Score remaining candidates**:
   - Direct topic match to a Core Interest Area or stated interest: high
   - Adjacent topic match: medium
   - Popular but topically unrelated: low
   - Keep only high and medium scores for the final list.

## Step 6: Fetch Context for Top Candidates

Fetch summaries for up to **4 show candidates** and **5 episode candidates** — these map directly to the Step 7 recommendation limits.

For episode candidates, call `get_episode_summary` with the episode `seq`.

For show candidates, use `list_podcast_episodes` with the show's `podcastSeq` to get a recent episode `seq`, then call `get_episode_summary` on it.

If a candidate episode is not processed and cannot be fetched, use the candidate source metadata only. Do not process episodes during a discovery session — the user has not indicated intent to consume these yet.

## Step 7: Present the Recommendations

Based on the user's answer in Step 3:
- **Shows only**: present only the New Shows to Follow section
- **Episodes only**: present only the Episodes Worth Trying section
- **Both**: present shows first, then episodes — these are separate tracks, a show recommendation does not duplicate an episode recommendation from the same podcast

Format the output using this template:

---

### Discover — {date}

_Based on your interests: {top 2–3 interests or topics from taste profile or Step 3}_

---

#### New Shows to Follow

For each recommended podcast (up to 4):

**{Podcast Name}**
{2–3 sentences on what the show covers and why it matches the user's taste specifically. Be concrete — name the host, the typical guest profile, or the format. Avoid generic phrases.}

Why for you: {one sentence connecting this show to a specific thing in the user's taste profile or stated interests.}

Follow now: {offer to call `set_podcast_follow` with `podcastSeq: {seq}`, `follow: true`} · https://app.podwise.ai/dashboard/podcasts/{seq}

---

#### Episodes Worth Trying

For each recommended episode (up to 5):

**{Episode Title}** · {Podcast Name} · {date}
{2–3 sentence summary grounded in `get_episode_summary` output.}

Why for you: {one sentence connecting this episode to the user's interests or gaps.}

[Open episode]({episode-url})

---

After the list, ask:
*"Want me to go deeper on any of these — fetch the full summary, highlights, or Q&A for a specific episode? Or would you like me to follow any of the recommended shows?"*

If the user says yes to following, call `set_podcast_follow` with the show's `podcastSeq` and `follow: true`.

## Common Failure Cases

- If `get_popular_episodes` and `ask_podwise` return only candidates that are already in the user's followed whitelist, tell the user: *"Your current subscriptions already cover this space well — here is what I found at the edges."* Present what there is rather than inflating the list.
- If the user has very narrow interests and the candidate pool after filtering is fewer than 3 items, tell them honestly and present what there is.
- If the user has no taste profile and refuses to provide interests, call `get_popular_episodes` and present the top 5 trending episodes with no personalisation — label them clearly as generic trending content, not personalised picks.
- If `taste.md`'s `_Last updated: {date}` is more than 60 days ago, note this at the top of the recommendations and suggest re-running `refine-taste` for fresher results.

## Output Contract

Produce one discovery digest per run.

Every recommendation must include a "Why for you" sentence grounded in the taste profile or the user's Step 3 answers — generic recommendations without a personalisation rationale are not acceptable.

Already-followed shows are never recommended. Shows in the Deprioritize list are never recommended.

The transcript is never fetched during a discovery session. Summaries are fetched from processed episodes only.

Always end with the follow-up prompt, which must include a "follow the show" option.
