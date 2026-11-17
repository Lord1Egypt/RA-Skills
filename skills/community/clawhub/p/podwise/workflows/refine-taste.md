# Podwise Refine Taste

Use this skill to construct a `taste.md` file that captures the user's podcast taste, topic interests, listening habits, and preferred output style. This file is read by other Podwise skills to personalize their outputs.

## Goals

1. Verify the Podwise MCP connection.
2. Collect the user's subscriptions and recent listening activity using the MCP tools.
3. Ask a small set of clarifying questions to fill in things the data cannot infer.
4. Write a `taste.md` file to the working directory.
5. Confirm where the file was saved and tell the user which skills will use it.

## Step 1: Check the Environment

Call `get_me`. If the Podwise tools are unavailable or return an authentication error, stop and follow [../references/installation.md](../references/installation.md) before continuing.

## Step 2: Gather Data

Call these tools to collect raw material for the taste profile:

- `list_followed_podcasts` with `days: 30` — the user's subscriptions (shows with recent activity as a proxy for the follow list).
- `list_my_episodes` with `type: "played"`, `pageSize: 50` — real listening behaviour (primary engagement signal).
- `list_my_episodes` with `type: "read"`, `pageSize: 50` — reading/exploration behaviour beyond regular listens.

Parse the results to extract:

- Podcast names, categories, and languages (from `list_followed_podcasts`)
- Which shows appear most frequently in listened episodes (strong engagement)
- Which shows are followed but never appear in history (low engagement — candidates for Deprioritize)
- Episode titles and topics from read episodes to understand what the user explores beyond their regular listens

If the user has many episodes, paginate with `page` until you have enough signal (a few hundred entries is plenty).

## Step 3: Ask Clarifying Questions

The data shows *what* the user subscribes to but not *why* or *how* they listen. Ask the following questions — all at once in a single message, not one by one:

1. **Topics you care about most**: Of the podcasts you follow, which topics or themes matter most to you right now? (e.g. AI, investing, language learning, startup building)
2. **Shows you actually listen to**: Are there shows you follow but rarely listen to, and shows you never miss? If so, which ones?
3. **Episode style preference**: Do you prefer long-form deep dives, short daily news, or interview-style conversations?
4. **Language setup**: Do you listen in multiple languages? If so, which is your primary learning language (if any)?
5. **What you do with insights**: Do you take notes, export to a PKM tool, or just listen? Which tool if any? (Notion, Obsidian, Logseq, Readwise)
6. **Output tone preference**: When Podwise AI summarizes or recommends things for you, do you prefer concise bullet points, flowing prose, or a mix?

## Step 4: Write taste.md

Synthesize the data and the user's answers into a structured file. Save it as `taste.md` in the current working directory unless the user specifies another path.

Use this template:

```markdown
# Listener Taste

_Last updated: {date}_

## Subscribed Podcasts

{List each podcast with name, category/topic, language, and a one-line note on how active the user is with it — inferred from recency of episodes in their feed.}

## Core Interest Areas

{2–5 topic areas the user cares about most, ranked by apparent priority. Derived from podcast categories + user's own answers.}

## Listening Style

- **Episode format preference**: {long-form / short daily / interview / mix}
- **Languages**: {primary language} {+ learning language if applicable}
- **Typical listening context**: {inferred or stated — e.g. commute, focused study, background}

## What the User Does with Insights

- **Note-taking**: {yes / no}
- **PKM tool**: {Notion / Obsidian / Logseq / Readwise / none}
- **Export habits**: {e.g. saves highlights, exports weekly recap, rarely exports}

## Output Preferences

- **Preferred format**: {bullet points / prose / mix}
- **Preferred summary length**: {short / medium / detailed}
- **Preferred language for AI output**: {language}

## Shows to Prioritize

{3–5 shows the user identified as ones they never miss. These should be weighted higher in catch-up, recap, and discovery outputs.}

## Shows to Deprioritize

{Shows the user follows but rarely engages with. Catch-up and recap should surface these last.}
```

Fill every section. If a field cannot be inferred and the user did not answer it, write `unknown` — do not omit the field.

## Step 5: Confirm and Summarize

After writing the file:

1. Print the full path where `taste.md` was saved.
2. Show the user a brief summary of what was captured: number of subscribed shows, core interest areas, and PKM tool detected.
3. Tell the user which skills will read this file automatically: `catch-up`, `weekly-recap`, `discover`, `topic-research`, `episode-debate`, `episode-notes`, and `language-learning`.
4. Suggest re-running this skill if their listening habits change significantly.

## Common Failure Cases

- If `list_followed_podcasts` returns an empty list, the user has no subscriptions yet. Ask them to follow at least a few podcasts in Podwise before running this skill.
- If the user skips the clarifying questions, write the taste profile from the data alone and mark skipped fields as `unknown`.
- If `taste.md` already exists, ask whether to overwrite or append before writing.

## Output Contract

Produce exactly one file: `taste.md`.

Do not print the full file contents in the conversation unless the user asks to review it — instead show the summary and the file path.
