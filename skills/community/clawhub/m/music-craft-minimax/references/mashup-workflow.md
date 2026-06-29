# Mashup Workflow

The signature feature of `music-craft-minimax`. A mashup combines two songs:

- **Song A** (content) — provides lyrics, structure, melody, emotional arc
- **Song B** (style) — provides instruments, era, mood, tempo, production style

The result is Song A's recognisable content in Song B's production style. This is the workflow that lets you make "Bohemian Rhapsody lyrics in reggaeton style" or "your favourite chanson in a modern electronic reimagining".

## When to Use Mashup

- The user wants two songs combined
- The user wants a recognisable song in a different genre
- The user wants the emotional arc of Song A preserved with a new production

## When NOT to Use Mashup

- The user wants a cover of one song (use cover workflow)
- The user wants standard generation with a style reference (use standard generation with `--references`)
- The user has no reference audio for either song (use standard generation)

## Decision Tree

```
Do you have Song A's original audio file or URL?
│
├── YES → Do you have custom lyrics (original or translated)?
│   │
│   ├── YES → ★ BEST: Cover Two-Step Workflow
│   │          1. music_cover_preprocess(audio_url) → cover_feature_id
│   │          2. Edit formatted_lyrics (add [Break], [Build Up] tags)
│   │          3. music_generation(model="music-cover", cover_feature_id, edited_lyrics, prompt)
│   │          Result: Preserves original MELODY + new STYLE + your LYRICS
│   │
│   └── NO  → Cover One-Step Workflow
│              1. music_generation(model="music-cover", audio_url, prompt)
│              2. MiniMax extracts lyrics via ASR + transforms style
│              Result: Preserves original MELODY + new STYLE + auto-extracted lyrics
│
└── NO  → Do you have lyrics?
    │
    ├── YES → Standard Generation
    │          1. Build production sheet prompt
    │          2. Structure lyrics with [Verse], [Chorus], [Break], [Build Up] tags
    │          3. music_generation(model="music-2.6", prompt, lyrics)
    │          Result: New melody (AI-generated) + your lyrics + target style
    │
    └── NO  → Auto Lyrics + Standard Generation
               1. (Optional) lyrics_generation(prompt) → structured lyrics
               2. music_generation(model="music-2.6", prompt, lyrics_optimizer=true)
               Result: Everything AI-generated from prompt only
```

**Key insight**: The **cover workflow** is the secret weapon for mashups. It preserves the original song's melody while changing style — this is what makes the result recognisable. Without it, you rely entirely on lyrics for recognition.

## Cloud Transmission Consent

> ⚠️ **The mashup workflow transmits both songs' audio, derived features,
> and lyrics to MiniMax.** Source audio for both Song A and Song B must
> be local files (URLs are not accepted in v1.5.0+). Before running:
>
> 1. Confirm you have the right to upload both songs to MiniMax.
> 2. Confirm the lyrics you submit (original, translated, or rewritten)
>    are yours or properly licensed.
> 3. The cover_feature_id and extracted lyrics may be retained by MiniMax
>    for up to 24 hours.
>
> If you do not want either song to leave your machine, do not use the
> cloud mashup path — there is no local-only mashup.

## Input Combinations

The mashup workflow accepts any combination of inputs for Song A and Song B. In v1.5.0+, all audio inputs must be local files (URLs are not accepted — use the private `music-source-fetch` skill to download a URL first).

| Song A | Song B | Possible? |
|--------|--------|-----------|
| Audio file | Audio file | ✅ best |
| Audio file | Song name | ✅ |
| Lyrics text | Song name | ✅ |
| Song name | Song name | ✅ (LLM knowledge only, no audio analysis) |
| Lyrics text | Lyrics text | ❌ use standard generation instead |

## Workflow: Both Songs Have Audio (Best Quality)

```bash
# Step 1: Get Song A's audio (must be a local file in v1.5.0+).
# If you only have a URL, download it first with the private music-source-fetch skill:
#   python3 ../music-source-fetch/scripts/fetch_by_title.py "Queen - Bohemian Rhapsody"
# Then use the resulting local path here.
SONG_A=/tmp/queen_bohemian_rhapsody.mp3

# Step 2: Get Song B's audio (same local-file rule applies)
SONG_B=/tmp/daddy_yankee_gasolina.mp3

# Step 3: Analyze both
python3 scripts/analyze_two_songs.py \
  --song-a "$SONG_A" \
  --song-b "$SONG_B" \
  --output /tmp/both_analysis.json

# Step 4: Analyze Song A's emotion (Song B's emotion optional)
python3 scripts/analyze_vocal_emotion.py "$SONG_A" --output /tmp/song_a_emotion.json

# Step 5: Build the prompt
python3 scripts/emotion_to_prompt.py \
  --emotion /tmp/song_a_emotion.json \
  --style /tmp/both_analysis.json \
  --language english \
  --output /tmp/mashup_prompt.json

# Step 6: Get Song A's lyrics (via ASR or manually)
# Option A: ASR via preprocess
curl -X POST https://api.minimax.io/v1/music_cover_preprocess \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "music-cover", "audio_url": "file:///tmp/queen_bohemian_rhapsody.mp3"}'
# Use the returned formatted_lyrics (with structure tags) or edit them.
# In v1.5.0+ audio_url must point to a local file the API can read (file://...),
# not a public streaming URL.

# Option B: User provides lyrics manually
LYRICS="[Verse]\nYour song A lyrics here\n\n[Chorus]\n..."

# Step 7: Generate the mashup using cover workflow (preserves melody)
COVER_ID="<from step 6 preprocess>"
PROMPT=$(jq -r '.final_prompt' /tmp/mashup_prompt.json)

curl -X POST https://api.minimax.io/v1/music_generation \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"music-cover\",
    \"cover_feature_id\": \"$COVER_ID\",
    \"lyrics\": $(echo "$LYRICS" | jq -Rsa .),
    \"prompt\": $(echo "$PROMPT" | jq -Rsa .),
    \"output_format\": \"url\",
    \"audio_setting\": {\"sample_rate\": 44100, \"bitrate\": 256000, \"format\": \"mp3\"}
  }"
```

## Workflow: Song A Audio + Song B by Name

```bash
# Step 1: Get Song A's audio (must be a local file in v1.5.0+).
# If you only have a URL, fetch it first with the private music-source-fetch skill:
#   python3 ../music-source-fetch/scripts/fetch_by_title.py "Adele - Someone Like You"
# Then use the resulting local path here.
SONG_A=/tmp/adele_someone_like_you.mp3

# Step 2: Analyze Song A
python3 scripts/analyze_vocal_emotion.py "$SONG_A" --output /tmp/song_a_emotion.json

# Step 3: LLM provides Song B's style from training data
# (no audio analysis for Song B)

# Step 4: Build the prompt manually using Song B's known style
# Confirm the vocal style and language with the user before locking the prompt.
PROMPT="<Song B style as confirmed with the user, including language and vocal style>"

# Step 5: Preprocess Song A for cover (audio_url must be file://... in v1.5.0+)
COVER_ID=$(curl -s -X POST https://api.minimax.io/v1/music_cover_preprocess \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"model\": \"music-cover\", \"audio_url\": \"file://$SONG_A\"}" \
  | jq -r '.cover_feature_id')

# Step 6: Generate
LYRICS="[Verse]\nSong A's lyrics in the target language\n\n[Chorus]\n..."

curl -X POST https://api.minimax.io/v1/music_generation \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"music-cover\",
    \"cover_feature_id\": \"$COVER_ID\",
    \"lyrics\": $(echo "$LYRICS" | jq -Rsa .),
    \"prompt\": $(echo "$PROMPT" | jq -Rsa .)
  }"
```

## Workflow: Both Songs by Name (LLM Knowledge Only)

```bash
# Step 1: No audio to download or analyze

# Step 2: LLM provides ALL features from training data
# Song A: lyrics, structure, emotional arc, melody (general)
# Song B: style, instruments, era, mood, tempo

# Step 3: Build the prompt from LLM knowledge
# No emotion analysis (no audio to analyze)
# Use the LLM's general sense of the song's vibe

# Step 4: Standard generation with the combined prompt
mmx music generate \
  --prompt "Style: similar to Song B (Bossa nova, João Gilberto, nylon guitar, light brushed drums, intimate). Lyrics: based on Song A's themes and emotional arc (melancholic, lost love in Paris). The result should preserve Song A's narrative while applying Song B's production style." \
  --lyrics "..." \
  --model music-2.6 \
  --out /tmp/mashup.mp3
```

This works best for well-known songs where the LLM has solid training-data knowledge. For obscure songs, ask the user for a brief description.

## Style Categories for Mashup

When Song B is identified, map to one of these style categories for the prompt:

| Category | Instruments | BPM | Mood |
|----------|-------------|-----|------|
| `french_chanson` | Accordion, strings, piano | 70–90 | Melancholic romantic |
| `rock` | Electric guitars, drums, bass | 120–150 | Energetic, powerful |
| `acoustic` | Guitar, light percussion | 80–110 | Intimate, warm |
| `epic_orchestral` | Full orchestra, choir | 60–85 | Cinematic, grand |
| `jazz` | Piano, brass, double bass | 140–180 | Smooth, swing |
| `latin` | Guitar, percussion, brass | 90–130 | Warm, passionate |
| `pop` | Synths, drums, bass | 100–130 | Catchy, upbeat |
| `blues` | Guitar, harmonica, bass | 70–100 | Soulful, gritty |
| `electronic` | Synths, drum machines | 110–140 | Atmospheric, pulsing |
| `ballad` | Piano, strings | 60–90 | Tender, emotional |

For sub-genres, see [`../music-craft/references/style-categories.md`](../../music-craft/references/style-categories.md).

## Quality Verification for Mashups

After generating, check:

1. **Recognition** — Would a friend say "That's [Song A]"?
2. **Style** — Would a friend say "but it sounds like [Song B]"?
3. **Emotion preservation** — Does the emotional arc match the original?
4. **Dynamic contrast** — Are quiet sections quiet and loud sections loud?
5. **Repetitive patterns** — Do repeated phrases intensify like the original?
6. **Vocal speed** — Do elongated sections stretch syllables like the original?
7. **Instrumentation** — Are instruments ALWAYS audible throughout? No a cappella sections unless intentional.
8. **Pauses** — Are there dramatic silence gaps between major sections?

If 3+ fail, the prompt was off. Adjust the emotion-to-prompt conversion parameters or the Song B style description.

## Edge Cases

### The user wants "Song A but in Song B's style with Song A's original lyrics"

Standard cover workflow with the original lyrics. No mashup needed.

### The user wants "Song A's melody but with new lyrics in Song B's language"

Cover workflow with translated lyrics. Preprocess Song A, translate lyrics to the target language, generate the cover.

### The user wants a 50/50 blend of two songs

This is the standard mashup. Use the decision tree, both songs by audio or by name.

### The user wants a mashup of three or more songs

Mashups with more than 2 songs are extremely hard to make recognisable. Recommend the user pick 2 songs and treat the third as an influence only.

### The user wants a mashup of two very different genres

Possible but challenging. The cover workflow helps by preserving the melody. The result may feel unusual — that's the point of a mashup. If the user wants a more accessible result, suggest a closer genre pair (rock + indie, pop + electronic, jazz + blues).

## Worked Example: Chanson + Reggaeton

User request: "Take 'Non, je ne regrette rien' by Édith Piaf and turn it into a reggaeton version."

Workflow:

1. Get the audio as a local file (URLs require `music-source-fetch` first in v1.5.0+).
2. Preprocess to extract lyrics (MiniMax ASR or user-provided):
   ```
   [Verse]
   Non, rien de rien
   Non, je ne regrette rien
   
   [Chorus]
   Ni le bien qu'on m'a fait
   Ni le mal tout ça m'est bien égal
   ```
3. Emotion analysis: detect Piaf's powerful, theatrical delivery with high vocal effort.
4. Style: reggaeton (perreo rhythm, 808 bass, Spanish vocals, 90–100 BPM).
5. Build the prompt:
   ```
   Reggaeton, dembow rhythm, 808 sub-bass, synth pads, Spanish male vocal,
   passionate and theatrical delivery like the original, 95 BPM in A minor,
   ALL instruments always playing throughout, never a cappella,
   full production, modern Latin radio mix
   ```
6. Generate via cover workflow (preserves Piaf's melody).
7. Verify: melody is recognisable, reggaeton rhythm is clear, theatrical delivery preserved.

## Key and BPM Compatibility Scoring

When `analyze_two_songs.py` is given both songs, it now scores their compatibility on two axes.

### Key Compatibility (Circle of Fifths)

Two keys are scored from 0.0 to 1.0:

| Distance | Score | Meaning |
|---|---|---|
| Same key | 1.0 | Perfect blend |
| Relative minor (e.g., A minor / C major) | 0.95 | Classic blend, very natural |
| 1-2 semitones (e.g., A minor / G major) | 0.8-0.9 | Close, easy transposition |
| 3 semitones | 0.7 | Transposition recommended |
| 4-5 semitones | 0.4-0.5 | Strong transposition needed |
| 6 semitones (tritone) | 0.3 | Clashing, both songs should transpose |

If the score is below 0.7, the output includes a `suggested transposition` note.

### BPM Compatibility

BPMs are scored as a ratio:

| Difference | Score | Meaning |
|---|---|---|
| 0% | 1.0 | Same tempo |
| <=15% | 0.7-1.0 | Natural blend |
| 15-30% | 0.4-0.7 | Moderate blend, tempo bridge may help |
| 30-50% | 0.1-0.4 | Requires time-stretching |
| >50% | 0.1 | Time-stretching essential |

### Output Format

```json
{
  "mashup_plan": {
    "target_bpm": 105.0,
    "compatibility": {
      "overall_score": 0.85,
      "bpm_score": 0.92,
      "key_score": 0.78,
      "key_distance_semitones": 2,
      "suggested_target_bpm": 105.0,
      "suggested_target_key": "A minor",
      "notes": [
        "BPMs (120 / 100) are within 20% - moderate blend",
        "Keys (A minor / B minor) are within 2 semitones - minor transposition may help",
        "Suggested transposition: A minor -> B minor (shift 1 semitones)"
      ]
    }
  }
}
```

The `notes` array is also appended to the final prompt as `mashup compatibility: ...` so the LLM and the music model see the guidance.

## Anti-Sparse for Mashups

Mashups are especially prone to sparse output because the model is being asked to do something unusual. The anti-sparse rules are critical:

- Always include: "ALL instruments ALWAYS playing throughout, NEVER go a cappella or silent"
- Always list every instrument from Song B's style
- For quiet sections, use explicit form: "quiet sections: reduced to [instruments] only, still fully played"
- Test with a short generation first; if sparse, adjust the prompt before the full version
