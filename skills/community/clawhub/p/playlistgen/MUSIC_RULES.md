# Music Rules

These rules are loaded by the music server at startup and injected into the LLM prompts.
Edit this file to change how the system interprets prompts and curates playlists — no code changes needed.

---

## Prompt Interpretation

**What it is:** When a user sends a playlist request, the first step is to convert the free-form text into structured music tags (genres, subgenres, moods, usage contexts, year, energy, language, regions, popularity). These tags are used to query the song database. The server sends the full catalog vocabulary to the LLM so it only returns tags that actually exist in the library.

**About catalog tags:** The catalog vocabulary is split into two tiers. *Regular tags* appear on the main line (sorted by frequency, most common first). *Long-tail tags* — those with a song count of 2 or fewer — appear on a separate `[LT]` line. Long-tail tags represent niche subgenres, rare moods, or micro-genres; include them deliberately when the request calls for something obscure or specific.

**Rules:**

- genres: pick 2 values (regular tags only, no long-tail)
- subgenres: pick 3 regular tags + 1 long-tail tag
- moods: pick 2 regular tags + 1 long-tail tag
- usage_contexts: pick 2 regular tags + 1 long-tail tag
- year: return a two-element list [start_year, end_year] spanning ~20 years if the prompt implies an era (e.g. "80s" → [1978, 1989], "turn of the millennium" → [1997, 2005]); otherwise return []
- energy: include one or more matching Energy values if the prompt implies energy level (e.g. "workout" → ["high"], "chill" → ["low", "medium"], "party" → ["high"]); otherwise return []
- language: include one Languages value if the prompt implies a specific language or language-tied genre (e.g. "Mandopop" → "Mandarin", "j-pop" → "Japanese"); otherwise leave empty
- regions: include matching Regions values if the prompt implies geography; otherwise leave empty
- popularity_hint: infer from cues — "underground/obscure/deep cuts" → "niche" or "obscure"; "hits/charts/popular" → "mainstream" or "popular"; "indie/alternative" → "indie"; otherwise "any"

Always return all 9 keys. Use "", [] for empty values, never null.
Only use values that appear verbatim in the catalog vocabulary (except year, which is a free integer range).
Return plain tag names only — no counts, no [LT] markers in the output.

---

## Final Playlist Curation

**What it is:** After candidate songs are fetched from the database, the LLM reviews them and selects a final ordered playlist. The LLM sees each song's genre, subgenre, mood, energy, language, region, year, and popularity, and picks the best tracks for a cohesive, diverse listening experience. Language, region, and popularity preferences from the interpretation step are passed as soft hints here.

**About track counts:** `{min_count}` is half of the requested playlist size (the minimum acceptable); `{max_count}` is the full requested size (default 30). Always try to reach `{max_count}`.

**Rules:**

- Select between {min_count} and {max_count} tracks
- HARD LIMIT: Never select more than 3 tracks from the same artist
- Maintain genre consistency (or subgenre consistency if the playlist targets a specific subgenre)
- Maximize artist diversity — avoid clustering the same artist back-to-back
- If the prompt implies a specific era (decade or period), prefer songs whose year falls in that range; otherwise spread across eras for variety
- If the prompt implies a specific region or culture, prefer songs from that region; otherwise spread across regions for variety
- If the prompt implies a popularity level (e.g. "obscure", "hits"), apply it as a strong preference; otherwise mix mainstream and niche tracks for variety
- Order for smooth energy and mood transitions
