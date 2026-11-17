# Podwise Weekly Recap

Use this skill to turn a week of scattered podcast listening into one coherent digest — what you heard, what you saved, and what was worth remembering. The output is ready to read as-is, forward to yourself by email, or drop into a PKM tool.

## Goals

1. Verify the Podwise MCP connection.
2. Load `taste.md` to determine the user's PKM tool and output format preference.
3. Fetch this week's episodes and highlights via the MCP tools.
4. Synthesize the material into a structured weekly recap.
5. Deliver the recap in the user's preferred format and offer to export it.

## Step 1: Check the Environment

Call `get_me`. If the Podwise tools are unavailable or return an authentication error, stop and follow [../references/installation.md](../references/installation.md) before continuing.

## Step 2: Load the Listener Taste

Look for `taste.md` in the current working directory.

- If found, read it silently. Use the **PKM tool**, **Output Preferences**, and **Core Interest Areas** sections to shape the recap's format, length, and framing.
- If not found, proceed with default formatting (prose summary, medium length) and note at the top of the output: *"No taste.md found — run `refine-taste` to personalise recap format and export destination."*

## Step 3: Determine the Recap Window

If the user did not specify a time range, default to the past 7 days.

Confirm with the user if the window is ambiguous — for example if today is mid-week (Tuesday–Thursday), ask whether they want this week so far (Mon–today) or the last 7 days.

## Step 4: Fetch This Week's Listening

Fetch from two sources:

- `list_my_episodes` with `type: "played"`, `pageSize: 50` — actual listening behaviour this week.
- `list_my_episodes` with `type: "read"`, `pageSize: 50` — episodes the user viewed but may not have listened to fully.

Parse each entry for: podcast name, episode title, publication date, and episode seq.

`list_my_episodes` returns the user's most recent play/read activity, newest first. Keep the episodes the user actually played or read within the recap window, regardless of the episode's original publication date — an older episode listened to this week still belongs in the recap. If the window is longer than the tool's recent-activity range, page through with `page` until entries fall outside the window.

**Fallback**: If the combined result after filtering is fewer than 5 episodes, supplement with:

- `list_followed_episodes` with `days: {window_days}`

Mark any supplement episodes as "not yet listened — published this week". If the total remains below 5 even after supplement, note at the top of the recap: *"Based on your subscriptions this week — your listening history was thin for this window."*

## Step 5: Fetch AI Outputs for Each Episode

For each episode that made it through the Step 4 filter, call `get_episode_summary` with the episode `seq` (includes summary, highlights, chapters, Q&A, keywords, and mind map).

If it fails for an episode because it has not been processed yet, include it in the recap with its podcast name, episode title, and a note: "not yet processed — [Open episode]({url})". This gives the user enough context to decide whether to process it manually.

**Silently record** every episode returned by `list_my_episodes` that did not make it into the Part 1 recap (activity outside the recap window, or entries that didn't make the cut). These go into an "Also in your history" section at the bottom of the recap — title, podcast name, and date only, no additional tool calls.

Do not call `process_episode` automatically during a recap.

## Step 6: Synthesize the Recap

Before writing, apply format preferences from the taste profile if loaded:

- If **Preferred format = bullet points**: write Part 1 summaries as bullet lists instead of prose
- If **Preferred summary length = short**: write 1–2 sentences per episode
- If **Preferred summary length = detailed**: retain 3–4 sentences per episode
- If **Preferred format = prose / mix**: keep the default prose format

Then synthesize in three parts:

### Part 1 — Episode by Episode

For each episode, produce a compact entry:

**▶ {Episode Title}** · {Podcast Name} · {date} *(listened)*  
or  
**👀 {Episode Title}** · {Podcast Name} · {date} *(read — viewed summary/highlights)*

{2–3 sentence summary}

Highlights:
- {highlight}
- {highlight}

[Open episode]({episode-url})

Order entries from most relevant to the user's **Core Interest Areas** down to least relevant, using the taste profile if loaded. Distinguish listened episodes (▶) from read-only episodes (👀) throughout.

### Part 2 — Themes of the Week

Look across all episodes and extract 2–4 recurring themes or ideas that appeared in multiple shows this week. Write 2–3 sentences on each theme, citing the 2–3 most relevant episodes per theme. This section transforms isolated episode content into a higher-level view of what the user's listening world was about this week.

If all episodes cover completely different topics with no overlap, skip this section and note: *"No recurring themes this week — your listening was varied."*

### Part 3 — Worth Revisiting

Pick highlights or ideas that stand out, in this priority order:
1. **Actionable** — anything with a clear next step or advice worth acting on
2. **Surprising** — ideas that challenge or reshape how you think
3. **Useful** — genuinely valuable knowledge that's worth remembering

Quantity rule (based on total episodes in Part 1):
- Fewer than 5 episodes → pick 1
- 5–10 episodes → pick 2
- More than 10 episodes → pick 3

Write one sentence per pick and link back to the source episode. This is the section the user is most likely to forward to a friend or paste into their notes.

## Step 7: Format and Deliver the Recap

Format the final output using this template:

---

## Weekly Podcast Recap — {week date range}

_{N} episodes · {M} shows · {week range}_

---

### This Week's Episodes

**▶ {Episode Title}** · {Podcast Name} · {date} *(listened)*
{2–3 sentence summary}

Highlights:
- {highlight}
- {highlight}

[Open episode]({episode-url})

---

{repeat for each episode (listened and read)}
{if any read-only episodes are included, tag them *(read)* instead of *(listened)*}

---

### Themes of the Week

**{Theme 1}**
{2–3 sentences. Mentioned in: {Episode A}, {Episode B}.}

**{Theme 2}**
{2–3 sentences. Mentioned in: {Episode C}.}

---

### Worth Revisiting

- **"{highlight or idea}"** — {Episode Title} · {one sentence on why it stands out}
- **"{highlight or idea}"** — {Episode Title} · {one sentence on why it stands out}

---

### Also in Your History

*{N} additional episodes from your history that were outside this recap's window or didn't make the cut:*

- **{Episode Title}** · {Podcast Name} · {date}
- **{Episode Title}** · {Podcast Name} · {date}

---

_Generated by podwise-weekly-recap · {date}_

---

After presenting the recap, ask the user:
*"Would you like to export this to {PKM tool from taste profile, or 'your PKM tool'}, share it, or save it as a plain text file?"*

## Step 8: Export the Recap

If the user confirms export, write the recap to a file named `weekly-recap-{YYYY-MM-DD}.md` in the current working directory.

If the user's taste profile specifies a PKM tool, remind them they can paste the file directly into:
- **Notion**: as a new page in their notes database
- **Obsidian**: as a new note in their vault
- **Logseq**: as a new journal page
- **Readwise**: via the Readwise import or daily highlights feature

Tell the user clearly that the recap file is the handoff.

## Common Failure Cases

- If all episodes in the window are unprocessed, there is nothing to synthesize. Offer to run the `catch-up` workflow first to process the week's episodes before generating the recap.
- If only one or two episodes are available, produce the recap as normal but skip the Themes section if there is insufficient material for cross-episode synthesis.
- If `taste.md` is missing, default formatting is fine — just note it at the top.
- If the user asks for a monthly recap instead, adjust the window to 30 days and update the output header accordingly.

## Output Contract

Produce exactly one recap document per run with three main sections: episodes, themes, and worth revisiting.

A fourth section ("Also in your history") is added whenever there are recorded history entries that did not make the episode list.

The themes section may be omitted only when there is genuinely no cross-episode material.

Always end with the export prompt. Always write the file if the user confirms export.
