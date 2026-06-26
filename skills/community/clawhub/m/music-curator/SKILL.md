---
name: music-curator
description: Curate personalized playlists and music recommendations with strict intent preservation. Use when the user wants a playlist, sequence, queue, recommendation set, artist/track expansion, or music discovery with taste and version constraints. Designed to work above playback/control skills like music-assistant and knowledge skills like lastfm/last-fm. Especially useful when the user cares about boundaries such as official songs only, no remixes/covers/instrumentals, role/character/theme songs, or similar-song expansion from seed tracks.
license: MIT
---

# Music Curator

Act as the **curation layer**, not the player and not the raw search engine.

## Core rules

**Do not broaden the request without permission.**

Examples:
- "VALORANT songs" does **not** mean "songs with a VALORANT vibe".
- "official songs" does **not** mean remixes, karaoke versions, instrumentals, or fan edits.
- "similar songs" **does** allow expansion beyond direct ownership/official affiliation.

**Do not let an earlier music task contaminate the current one.**

Examples:
- A previous seed-track expansion task must not narrow a later franchise playlist task.
- A previous "strict official songs" task must not constrain a later "give me similar songs" task.

Treat each new playlist/recommendation request as a fresh classification unless the user explicitly says to continue the previous one.

If the request is ambiguous, classify it before curating.

## Request classification

Classify each request into one of these modes:

1. **Strict identity**
   - The user wants songs that truly belong to a franchise, artist era, soundtrack, event, character, or official release family.
   - Examples: "无畏契约的歌", "周杰伦电影主题曲", "官方赛事曲".
   - In this mode, do **not** use similarity as the final selector.
   - Use external/music-knowledge skills only to verify identity and enumerate the canonical candidates.

2. **Similarity / expansion**
   - The user wants more songs *like* a seed song/artist/mood.
   - Examples: "按这首歌扩 15 首", "类似这个 vibe", "更冷一点但同气质".
   - In this mode, use `lastfm` as the primary discovery engine by default. Only fall back to `last-fm` if `lastfm` is unavailable or insufficient.

3. **Hybrid**
   - The user wants a strict core plus controlled expansion.
   - Example: "先放官方曲，再混 5 首同风格".

If unsure, ask one short clarifying question before generating a queue.

## Tool roles

Use tools/skills with this division of labor:

- **music-assistant**: playback, queue management, device control, library/provider lookup, final enqueue.
- **lastfm**: default music-knowledge and discovery source for similarity, related artists/tracks, popularity context, discovery support, and listening-profile support.
- **last-fm**: fallback/reference-only companion skill when `lastfm` is unavailable or when broader API reference coverage is needed.
- **This skill**: intent preservation, filtering, sequencing, taste logic, version hygiene, and final candidate selection.

Do not let raw search results define meaning when the user asked for a strict category.

## Default version hygiene

Unless the user explicitly asks otherwise, filter out:
- remix
- remaster (if materially different and the original is available)
- karaoke
- piano
- instrumental
- 8-bit
- slowed / reverb / sped up / nightcore
- bootleg / mashup / fan edit
- clearly fan-made derivatives

Do **not** auto-ban `TV size` or `cover` just because of the label.

Instead, evaluate them by release context:
- Keep them when they are clearly official or formally released within the franchise/project.
- Exclude them when they are obvious unofficial derivatives, fan uploads, or low-signal search noise.

Do **not** auto-ban `live` or `acoustic` either; only exclude them when they are clearly off-brief for the user's request or when a more canonical version is available and the user did not ask for alternates.

If only non-ideal versions are available, say so explicitly before queueing them.

## Curation workflow

### A. Strict identity workflow

Use this when semantic precision matters more than quantity.

1. Identify the exact category the user means.
2. Build a candidate list from reliable music knowledge sources or trusted skill outputs.
3. Verify each candidate against the user's boundary.
4. Remove version-noise by default.
5. Use **Music Assistant search as the playback entrypoint**:
   - search first
   - choose the cleanest matching result
   - then enqueue/play
   - do not prefer blindly reusing old naked URIs when fresh search results are available
6. If a chosen provider version errors at playback time, retry with another clean search result/provider mapping before giving up.
7. If Music Assistant lacks some canonical tracks, report the gap instead of silently substituting unrelated songs.

### B. Similarity workflow

Use this when the user wants discovery/expansion.

1. Take one or more seed tracks/artists.
2. Pull related tracks/artists/tags from discovery sources.
3. Filter by the user's hidden defaults:
   - avoid noisy versions
   - avoid obvious repeats
   - keep energy/mood aligned unless asked to vary
4. Build a set with light shape:
   - open familiar
   - expand outward gradually
   - avoid five near-duplicates in a row
5. Send the final set to Music Assistant.

### C. Hybrid workflow

1. Start with a strict canonical core.
2. Mark where expansion begins.
3. Add similarity-based tracks only after the strict core.
4. Keep those sections mentally and verbally separate.

## Queue-building rules

When assembling a playlist/queue:
- Avoid duplicate songs across providers unless the user asked for alternates.
- Prefer the provider/version most likely to be the original intended release.
- Balance tempo and energy unless the user asked for a monotone block.
- Avoid abrupt quality drops.
- If the user asks for a number (e.g. 20 songs), do not fill with junk merely to hit the count.
  - Prefer: "I found 13 clean fits; I can add 7 looser fits if you want."
- For playback requests, **start playback quickly**:
  - first push a small set of high-confidence tracks so music starts immediately
  - then continue filling the queue toward the requested size
  - do not wait to finish perfect curation before starting playback
- Build a larger candidate pool than strictly needed, then filter/resolve from that pool instead of adding one song at a time with long pauses.

## Communication rules

Before queueing, provide one of these depending on confidence:

- **High confidence**: a concise explanation of selection logic, then queue.
- **Medium confidence**: a candidate list first, then queue after confirmation.
- **Low confidence**: ask one focused question.

When the user clearly wants playback now, prefer a short acknowledgment plus immediate queue action over a long analysis dump.

During long queue-building work, provide only concrete progress updates:
- what is already queued
- what was just added
- what was excluded and why

Never present a vibe-expansion set as if it were a strict official set.

## User-specific defaults to preserve

When working for this user, assume:
- Intent preservation matters more than clever expansion.
- If not explicitly requested, avoid remix / cover / piano / instrumental / karaoke / fan-edit variants.
- For franchise/theme requests, official identity comes before mood similarity.
- For recommendation requests, it is okay to use similarity/discovery tools **after** the request is clearly similarity-based.

## Output style

When listing curated results, keep it clean:
- `Track — Artist`
- Optionally add short reason tags like `(official)`, `(seed-adjacent)`, `(closer/looser fit)`.

If some tracks are unavailable in Music Assistant, separate:
- **Canonical matches found in MA**
- **Canonical matches missing in MA**

## Failure modes to avoid

Bad behavior:
- User: "Play VALORANT songs"
- Assistant: adds unrelated cyber/EDM tracks because they feel similar.
- User: after a `Die For You` similarity test, asks for "VALORANT songs"
- Assistant: keeps using `Die For You` as a hidden seed and narrows the later task incorrectly.
- User wants music now
- Assistant: spends many minutes debating edge cases instead of queueing the obvious tracks first.

Correct behavior:
- Build the strict VALORANT set first.
- If the user wants more after that, ask whether to expand into similar tracks.
- Reset task scope between separate music requests unless continuation is explicit.
- Start playback with high-confidence tracks, then continue filling the queue.
