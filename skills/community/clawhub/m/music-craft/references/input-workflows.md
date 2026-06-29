# Input Workflows

The skill can accept music generation requests in several distinct shapes (Input Types 1, 2, 3, 5, 6, 7, 7b, 9 — the audio-download and image types were removed in v1.5.0). The Pre-Flight Check applies regardless, but the workflow loop changes slightly per input. Types 1–5 are self-contained; types 6, 7, 7b, and 9 use free runtime tools to enrich the context.

## Analyzing Source Material

If the user provides source audio or an analysis file, extract the reusable facts before writing the prompt:

- Use user-provided analysis when available.
- Use song-folder notes such as `info.txt` when available; they often contain
  source URL, release notes, BPM, key, instrumentation, and prior prompt
  history.
- Treat `lyrics_whisper_medium.json` as a valid lyrics input. Its segment
  timestamps can help place section tags in long transcripts.
- If `music-craft-minimax` is installed, its analysis scripts can extract tempo, key, sections, instrumentation, vocal traits, and energy curve.
- If ACE-Step is already running, its audio-understanding mode can provide basic BPM, key, time signature, and caption without installing a separate analysis stack.
- If there is no source material, continue with the request text and inferred defaults.

Do not block a standard text-only song request just because no audio analysis exists.

For transcript cleanup, canonical section tags, and song-folder note handling,
load [`lyrics-cleanup.md`](lyrics-cleanup.md).

### Mandatory confirmations after source analysis

- If vocals are unclear, confirm vocal vs instrumental before prompt writing.
- If source duration exists but user intent does not, confirm target length before generation.
- Do not treat analyzer uncertainty as permission to choose instrumental mode.

## Signal-Extraction Rubric

Before asking follow-up questions, classify the request and extract the minimum useful fields:

| Class | What it means |
|---|---|
| Standard song | Original track from a style brief, with or without auto-lyrics |
| User lyrics | The user already provided the words to sing |
| Instrumental | No vocals, no lyric drafting |
| Text-only reference | Song name, artist, era, or genre as a vibe cue only |
| URL/image enrichment | Removed in v1.5.0 — local audio files only |
| MiniMax redirect | Fast cloud cover, mashup, advanced analysis, or separate `mmx` flag control |
| ACE-Step local audio | Local source-audio cover/repaint experiment after hardware/time-budget gate |

Extract these fields before asking:

- language
- genre
- mood
- theme
- duration
- lyrics source
- vocal or instrumental mode
- references

Confidence labels:

| Confidence | Meaning |
|---|---|
| Clear | Explicitly stated by the user |
| Inferred | Reasonable from the wording or context |
| Missing | Not present yet; ask or fill from defaults |
| Conflicting | Two signals disagree; pause and resolve before generating |

## Decision Tree

```
What did the user provide?
├── A clear description (style, mood, language)
│   └── → Input Type 1: Description only
├── Lyrics text
│   └── → Input Type 2: User-provided lyrics
├── A local audio file
│   └── → Input Type 3: source audio (local ACE-Step experiment or MiniMax redirect)
├── Just a song name or artist
│   └── → Input Type 5: Reference only
├── A URL to a lyrics page
│   └── → Input Type 6: Lyrics URL (web_fetch)
├── A YouTube URL (metadata only)
│   └── → Input Type 7: YouTube metadata (web_fetch)
└── A genre or cultural reference (no song)
    └── → Input Type 9: Genre context (web_search + web_fetch)
```

## Input Type 1: Description only

**Example:** "Make a sad love song in Spanish."

**Workflow:**

1. Auto-detect: language (ES), genre (romantic ballad), mood (sad), duration (~3 min).
2. Ask 1–3 questions for the ambiguous parts (lyrics source, vocal register, reference artist).
3. Build the prompt.
4. Generate.

**Most common case.** Standard workflow.

## Input Type 2: User-provided lyrics

**Example:** "Here's a poem I wrote. Turn it into a rock anthem with female vocals in Spanish."

**Workflow:**

1. Take the user's text AS-IS for the lyrics body.
2. Auto-detect: genre (rock anthem), vocal (female, Spanish), duration (~3 min).
3. Add section tags to the lyrics without altering the words. If the text is long, split it into verse / chorus / bridge heuristically. If short, repeat the chorus 2–3 times.
4. Build the prompt with the lyrics body.
5. Generate.

**Common mistake:** Altering the user's words. Do not paraphrase, do not "improve" their phrasing. Add tags and structure; leave words alone.

If the lyrics came from ASR/Whisper, clean transcript artifacts before adding
final tags. See [`lyrics-cleanup.md`](lyrics-cleanup.md).

### Heuristics for splitting long text

If the user provides prose and asks for a song:

- **> 500 words:** Write summary lyrics, do not set the whole text to music (would be 20+ minutes)
- **200–500 words:** Pick 2–3 key passages, set those as the verses, write a separate chorus
- **< 200 words:** Use most of it, split into 2 verses + 1 chorus
- **< 50 words:** Use it as a chorus, write 2 verses around it

Always ask: "Your text is long. Do you want me to set it all, summarize it, or pick the most lyrical passages?"

## Input Type 3: Reference audio file

**Example:** User attaches an MP3 of a song they like.

Choose the route from the user's priority:

- **Local, no cloud, exact source-length experiment:** use ACE-Step audio-conditioned generation in [`acestep-generation.md`](acestep-generation.md). Confirm the user accepts slower queue-bound behavior and hardware/timeout constraints.
- **Fast cloud cover, advanced analysis, emotion extraction, or mashup:** switch to `music-craft-minimax`.

**MiniMax redirect message:** "That needs fast cloud cover / style transfer or advanced audio analysis, which is in `music-craft-minimax`. Switch to that skill and I will run the same pre-flight with the extended checks."

**Local ACE-Step message:** "I can try this locally with ACE-Step cover/repaint. It is slower and experimental; I will trim long sources or raise the server timeout before starting."

**Within music-craft-minimax**, use the `analysis_orchestrator.py` script to handle advanced analysis in one step:

```bash
# One command: get the full analysis JSON
python3 scripts/analysis_orchestrator.py --audio /tmp/song.wav --output /tmp/analysis.json

# This runs analyze_vocal_emotion.py + analyze_audio.py + any optional features (CLAP, autochord, allin1, pyloudnorm)
# and produces a unified JSON ready for emotion_to_prompt.py
```

The orchestrator supports:
- `--audio` (one or more, for mashups)

After analysis, the typical flow is:
1. Run `analysis_orchestrator.py` → unified JSON
2. Run `emotion_to_prompt.py --emotion [json] --style [json]` → final prompt
3. Call `mmx music generate`, `music_generate`, MusicGen, or the detected backend with the prompt

## Input Type 5: Song name or artist reference

**Example:** "Make a song like 'Bohemian Rhapsody'." or "Something that sounds like Rosalía."

**Workflow:**

1. Use LLM knowledge of the named song or artist to infer style, structure, and mood.
2. If the song is well-known and LLM has solid knowledge, skip the next step.
3. If the song is obscure or recent, `web_search` for "[song/artist] analysis style" → `web_fetch` a music blog.
4. Ask the user: "Do you want the same lyrics, similar lyrics, original lyrics in a similar style, or instrumental?"
5. Build the prompt using the inferred style.
6. Generate.

**Limitations:** LLM knowledge is approximate for very recent or obscure songs. Web search helps but is not a substitute for listening to the actual song.

### How to use LLM knowledge for style inference

When the user names a song or artist, distill:

- **Genre and sub-genre:** from the artist's typical catalog
- **Typical instruments:** from the production style
- **Typical BPM range:** from the artist's tempo
- **Vocal style:** male/female/group, language, register
- **Lyrical themes:** common topics in the artist's work
- **Production quality:** lo-fi, polished, cinematic, raw

Then map to a production-sheet prompt. Example: "Bohemian Rhapsody" → epic rock, multi-section, choir, dramatic dynamics, ~6 min.

## Input Type 6: Lyrics URL

**Example:** "Make a song using these lyrics: https://genius.com/Queen-bohemian-rhapsody-lyrics"

**Workflow:**

1. `web_fetch` the URL.
2. Extract the lyrics text from the page. Common selectors / patterns:
   - genius.com: lyrics are in `<div data-lyrics-container="true">` or similar
   - letras.com: lyrics in `<div class="lyric-original">` or `<div id="letra">`
   - azlyrics.com: lyrics in a `<div>` with no useful class, but the page has no chrome around them
3. Clean up: remove "[Verse]", "[Chorus]" tags if present (we add our own), remove ads, navigation, comments.
4. If the page returns only chrome or JS-loaded content, fall back to `browser` to drive the page.
5. Treat the cleaned text as Input Type 2 (user-provided lyrics).
6. Auto-detect or ask for style.
7. Build the prompt and generate.

**Privacy note:** Use the fetched lyrics as inspiration for style and structure. Do not paste copyrighted lyrics verbatim into the song unless the user explicitly says it's OK (e.g., public domain, their own writing, or they have rights).

### Sites that work well with `web_fetch`

- genius.com — usually works, lyrics are in the HTML
- letras.com — works, lyrics in a clean div
- lyricsmode.com — works
- songlyrics.com — works
- azlyrics.com — works, minimal chrome
- musixmatch.com — partial, may need browser

### Sites that need `browser` fallback

- Spotify (lyrics may be JS-loaded)
- YouTube Music
- Apple Music web

## Input Type 7: YouTube URL (metadata only)

**Example:** "Make a song like this one: https://youtube.com/watch?v=..."

**Workflow:**

1. `web_fetch` to `youtube.com/watch?v=...`.
2. Extract from the HTML / OG tags:
   - **Title** (usually in `<title>` or `og:title`)
   - **Channel name** (in `linkedSchema` or `author`)
   - **Description** (in `og:description` or the page body)
   - **View count** (if available)
   - **Hashtags** (in description)
   - **Related videos** (for genre/era inference)
3. Optionally `web_search` for "[channel name] genre style" to confirm.
4. LLM infers style, era, mood from the metadata.
5. Ask the user: "Based on the video '[title]' by [channel], I'll make [inferred style]. Sound right? Or do you want a different angle?"
6. Build the prompt and generate.

**No audio is downloaded** in this workflow. The metadata is enough to inform the prompt.

**v1.5.0+:** `web_fetch` for YouTube/JioSaavn pages returns metadata only (artist, title, era). It does not download audio. To get the audio, use the private `music-source-fetch` skill first.

**When to redirect to music-craft-minimax:** If the user wants the actual audio of the YouTube video (for cover, sample, or detailed analysis), use the `music-source-fetch` skill to download the audio to a local path first, then proceed as Input Type 3.

## Input Type 7b: JioSaavn URL (metadata only)

**Example:** "Make a song like this one: https://www.jiosaavn.com/song/..."

**Workflow:**

1. `web_fetch` to the JioSaavn URL.
2. Extract from the HTML / OG tags:
   - **Title** (track name)
   - **Artist** (album artist or primary performer)
   - **Album** (if available)
   - **Language** (often inferable from the artist or album)
   - **Description** (if available)
3. For Bollywood and Indian regional music, JioSaavn has deeper catalog coverage than YouTube. Use this when the user names an Indian song that is not easily found on YouTube.
4. LLM infers style, era, mood from the metadata.
5. Ask the user: "Based on the track '[title]' by [artist], I'll make [inferred style]. Sound right?"
6. Build the prompt and generate.

**No audio is downloaded** in this workflow. The metadata is enough to inform the prompt.

**v1.5.0+:** `web_fetch` for JioSaavn pages returns metadata only (artist, title, language, album). It does not download audio. To get the audio, use the private `music-source-fetch` skill first.

**When to redirect:** If the user wants the actual audio of the JioSaavn track (for cover, sample, or detailed analysis), use the `music-source-fetch` skill to download the audio to a local path first, then proceed as Input Type 3.

## Input Type 9: Genre or cultural reference (no song)

**Example:** "I want a song in the style of 80s Italo disco" or "Make a Brazilian bossa nova song."

**Workflow:**

1. `web_search` for the genre or culture + "characteristics" or "history".
2. `web_fetch` Wikipedia or a music blog from the top results.
3. Extract:
   - **Typical BPM range**
   - **Characteristic instruments**
   - **Era and production style**
   - **Vocal conventions** (language, register, ornamentation)
   - **Lyrical themes** (if relevant)
4. Build a production-sheet prompt using the extracted context.
5. Confirm with the user before generating.

### Example: "80s Italo disco"

After web research:

```
Italo disco: 1980s European electronic dance music, characterized by:
- BPM: 110-130
- Instruments: analog synthesizers, drum machines (LinnDrum, Roland TR-808),
  arpeggiated synth bass, electronic percussion, vocoder, female vocals
- Production: gated reverb drums, lush pads, melodic basslines
- Era: 1983-1989, primarily Italian and German labels
- Mood: euphoric, romantic, danceable
- Vocals: often English or Italian, breathy female soprano
```

Built prompt:

```
Italo disco, 1980s European dance music, euphoric romantic mood, breathy female soprano vocal in English or Italian,
analog synthesizers, LinnDrum, TR-808 drum machine, arpeggiated synth bass, electronic percussion, vocoder, lush pads,
ALL instruments always playing throughout, never drop to a cappella,
120 BPM in C minor,
intro-verse-pre chorus-chorus-verse-chorus-bridge-chorus-outro with classic gated reverb on drums,
wide lush soundscape, 1980s analog production quality,
AVOID sparse arrangements, AVOID modern digital sounds, AVOID minimalist sections
```

## Edge Cases

### The user mixes input types

Example: "Here's a YouTube link. I want a French chanson version with these lyrics: [lyrics]."

This is Input Type 7 (YouTube metadata) + Input Type 2 (user lyrics). Use metadata for style, lyrics for body. Generate as standard.

If the user also wants the actual audio of the YouTube video, use the private `music-source-fetch` skill to download it locally first, then proceed as Input Type 3.

### The user provides a long prose document

Example: "Here's a 2000-word short story. Make a song about the main character."

This is a variant of Input Type 2. The skill should:

1. Read the prose.
2. Identify the central theme, the emotional arc, and any quotable phrases.
3. Write a short set of lyrics (verse-chorus-verse-chorus-bridge-chorus, ~3 min) that captures the theme.
4. Tag the structure.
5. Generate.

Do not try to set the entire 2000-word prose to music. That would be a 30-minute song.

### The user provides a chord progression

Example: "Make a song in C major with vi-IV-I-V."

This is musical theory input. The skill should:

1. Note the chord progression in the prompt (e.g., "verse: vi-IV-I-V in C major").
2. Ask: lyrics or instrumental? Style?
3. Generate.

Most providers do not respond well to raw chord notation; phrase the chords musically in the prompt instead.

### The user provides a melody (audio or MIDI)

This is Input Type 3. Redirect to music-craft-minimax — covers are the only way to use a specific melody.

### The user provides only a mood or vibe

Example: "Make something that feels like a Sunday morning in autumn."

This is Input Type 1 with a non-literal description. The skill should:

1. Map the vibe to style: "Sunday morning autumn" = warm, acoustic, soft, slightly melancholic.
2. Pick a default from [`style-categories.md`](style-categories.md) (likely `acoustic` or `lofi`).
3. Auto-generate lyrics around the vibe.
4. Generate.

### The user provides multiple conflicting inputs

Example: "Make a happy sad song in Spanish about leaving home but staying."

The "happy sad" oxymoron is a real creative direction. The skill should:

1. Recognize the tension.
2. Map to: minor key, mid-tempo, building structure (sad start, hopeful end), 2–3 mood adjectives (bittersweet, hopeful, melancholic).
3. Generate and let the user iterate.

Do not ask the user to resolve the contradiction — the tension is the creative direction.

### The user gives a URL that 404s or returns empty

Fall back to: "I couldn't fetch that URL. Can you paste the lyrics / describe the song / give me the title?" Then proceed as the appropriate Input Type.

### The user gives a non-music URL

`web_fetch` is generic — it will return whatever the URL has. If the user gives a non-music URL (e.g., a news article), say: "That doesn't look like a music source. Did you mean to give me a lyrics page or a YouTube link? Or did you want to make a song about [topic of the URL]?"

If the user does want a song about the topic, use the URL content as THEMATIC inspiration, not lyrics or melody.
