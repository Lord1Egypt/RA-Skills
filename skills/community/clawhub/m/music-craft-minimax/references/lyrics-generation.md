# Lyrics Generation API

MiniMax has a dedicated `lyrics_generation` endpoint that produces structured lyrics (with `[Verse]`, `[Chorus]`, etc. tags) from a theme prompt. This is more controllable than the implicit `lyrics_optimizer: true` behavior of `music_generate` — you can preview, edit, and iterate on the lyrics before generating the song.

## Endpoint

```
POST https://api.minimax.io/v1/lyrics_generation
```

## Modes

### `write_full_song` — Create from scratch

Generate a complete song from a theme prompt. The output is structured lyrics with section tags.

**Request:**

```bash
curl --request POST \
  --url https://api.minimax.io/v1/lyrics_generation \
  --header "Authorization: Bearer $MINIMAX_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "mode": "write_full_song",
    "prompt": "A French chanson ballad about lost love in Paris, melancholic romantic, theatrical, with accordion and strings",
    "title": "Nuit Parisienne"
  }'
```

**Response:**

```json
{
  "song_title": "Nuit Parisienne",
  "style_tags": "french chanson, melancholic, romantic, 80 BPM",
  "lyrics": "[Intro]\n\n[Verse]\nLes rues de Paris se taisent\nSous la lune qui s'éteint\n\n[Pre Chorus]\nEt mon cœur cherche ta voix\nDans le silence de la nuit\n\n[Chorus]\nNuit Parisienne, où es-tu?\nSans toi la ville n'est plus rien\n\n[Break]\n\n[Verse]\nLes cafés ferment leurs portes\nComme mes bras se ferment sur rien\n\n[Bridge]\nEt je marche, et je cherche\nUn écho de notre histoire\n\n[Chorus]\nNuit Parisienne, où es-tu?\nSans toi la ville n'est plus rien\n\n[Outro]\nNuit Parisienne..."
}
```

The `lyrics` field is ready to pass directly to `music_generate` or `mmx music generate`.

### `edit` — Modify existing lyrics

Modify existing lyrics. Use to iterate on auto-generated lyrics, fix awkward phrases, change the chorus, or shift the ending.

**Request:**

```bash
curl --request POST \
  --url https://api.minimax.io/v1/lyrics_generation \
  --header "Authorization: Bearer $MINIMAX_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "mode": "edit",
    "prompt": "Continue with a stronger chorus and a hopeful ending",
    "lyrics": "[Verse]\nI walked alone beneath the rain\nEvery window knew my pain\n\n[Pre Chorus]\nAnd the city held its breath tonight\n\n[Chorus]\nI am lost, I am cold",
    "title": "Midnight Rain"
  }'
```

**Response:**

```json
{
  "song_title": "Midnight Rain",
  "lyrics": "[Verse]\nI walked alone beneath the rain\nEvery window knew my pain\n\n[Pre Chorus]\nAnd the city held its breath tonight\n\n[Chorus]\nI am lost, I am cold\nBut the dawn is breaking through\nTomorrow I'll find my way\n\n[Bridge]\nThe city wakes, the lights return\nAnd the night releases me\n\n[Chorus]\nI am lost no more, I am whole\nThe dawn has broken through\n\n[Outro]\nMidnight rain, farewell to you"
}
```

The `edit` mode extends the lyrics, keeping the existing content and adding new sections. It does not rewrite what you give it.

## Parameters

| Parameter | Required | Description |
|---|---|---|
| `mode` | Yes | `write_full_song` or `edit` |
| `prompt` | Yes | Theme or style instruction, max 2000 chars |
| `lyrics` | `edit` mode only | Existing lyrics, max 3500 chars |
| `title` | Optional | Song title (preserved if provided) |

## When to Use

### Use `write_full_song` when:

- The user wants lyrics but has not provided any
- The user wants a specific theme ("a song about leaving home") with auto-generated lyrics
- You want to preview the lyrics before committing to generation
- The user wants to see options and choose one

### Use `edit` mode when:

- The auto-generated lyrics are close but need a tweak
- The user wants to add a bridge or modify the chorus
- The user wants to shift the ending (sad → hopeful)
- You want to translate the lyrics to another language

### Use neither (use `music_generate` with `--lyrics-optimizer`) when:

- The user does not care about specific lyrics
- You are generating many variations and lyrics quality is secondary
- The runtime's `music_generate` tool already handles lyrics generation internally

## Workflow: Preview Lyrics Before Generation

```bash
# Step 1: Generate lyrics preview
LYRICS=$(curl -s -X POST https://api.minimax.io/v1/lyrics_generation \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "write_full_song",
    "prompt": "Upbeat pop about summer road trips, English, 120 BPM",
    "title": "Highway Lights"
  }')

# Step 2: Extract lyrics from response
LYRICS_BODY=$(echo "$LYRICS" | jq -r '.lyrics')

# Step 3: Show user for approval
echo "$LYRICS_BODY"

# Step 4: If approved, generate the song
mmx music generate \
  --prompt "Upbeat pop, summer, road trip, 120 BPM in C major, electric guitar, synths, drum machine, bass, handclaps" \
  --lyrics "$LYRICS_BODY" \
  --model music-2.6 \
  --out /tmp/highway_lights.mp3
```

## Workflow: Iterate via Edit Mode

```bash
# Step 1: Generate base lyrics
LYRICS=$(curl -s -X POST https://api.minimax.io/v1/lyrics_generation \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "write_full_song",
    "prompt": "Melancholic ballad about a long-distance relationship, English",
    "title": "Far Away"
  }')

# Step 2: User reviews, wants a more hopeful chorus
# Step 3: Edit to strengthen chorus
EDITED=$(curl -s -X POST https://api.minimax.io/v1/lyrics_generation \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg lyrics "$(echo "$LYRICS" | jq -r '.lyrics')" --arg title "Far Away" '{
    mode: "edit",
    prompt: "Make the chorus more hopeful, add a bridge with a memory flashback",
    lyrics: $lyrics,
    title: $title
  }')")

# Step 4: Use edited lyrics for generation
LYRICS_BODY=$(echo "$EDITED" | jq -r '.lyrics')
mmx music generate \
  --prompt "Melancholic but hopeful ballad, English, 80 BPM, piano, strings, soft bass" \
  --lyrics "$LYRICS_BODY" \
  --model music-2.6 \
  --out /tmp/far_away.mp3
```

## Style Guidance in the Prompt

The `prompt` field in `lyrics_generation` is a free-form style instruction. The more specific, the better the output.

| Vague prompt | Better prompt |
|---|---|
| "A love song" | "A 1990s R&B slow jam about rekindling an old flame, with metaphors of seasons changing" |
| "A sad song" | "An indie folk ballad about losing a parent, sparse imagery of empty rooms, first person, 6 verses" |
| "A party song" | "A 2000s pop-punk anthem about sneaking out at night, hyperactive energy, call-and-response chorus" |
| "Una canción alegre" | "Un corrido tumbado alegre sobre celebrar la vida en la playa, ritmo bailable, vocales masculinas" |

The `title` is preserved if provided. The output lyrics are structured and tagged.

## Limits

- `prompt` max 2000 chars
- `lyrics` max 3500 chars
- No explicit duration control — length is determined by the prompt and the structure the model chooses
- Output language follows the prompt's language; specify explicitly if not English

## Common Issues

| Issue | Fix |
|---|---|
| Output lyrics are in wrong language | Specify the language explicitly in the prompt: "in French", "en español", "auf Deutsch" |
| Output is too short | Add to the prompt: "with at least 3 verses, 2 choruses, and a bridge" |
| Output is too long | Add: "concise, 2 verses and 1 chorus" |
| Chorus is weak | Use `edit` mode with: "Make the chorus stronger and more memorable" |
| Wrong emotional tone | Adjust mood adjectives in the prompt: "melancholic and resigned" vs "melancholic but hopeful" |
| Lyrics are too AI-generic | Add specific imagery or narrative: "mention a specific place, a specific time of day, a specific object" |

## Integration with Cover Workflow

For cover with translated lyrics:

1. Preprocess the cover (gets original lyrics via ASR)
2. Translate the original lyrics to the target language (with the LLM)
3. Edit mode to clean up the translation
4. Generate the cover with the translated lyrics

This produces covers that preserve the melody AND have native-quality lyrics in the target language.

## Web Lyrics Lookup

Removed in v1.5.0. Web lyrics lookup (LRCLib) moved to the private
`music-source-fetch` skill. In this skill, Whisper transcription of a
local audio file is the only lyrics source. If you need LRCLib-quality
lyrics for a known mainstream track, fetch them with `music-source-fetch`
first, then pass the resulting lyrics file path into this skill.
