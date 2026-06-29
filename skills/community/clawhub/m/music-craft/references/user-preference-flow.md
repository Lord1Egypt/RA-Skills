# User Preference Flow

The skill does not start with a questionnaire. It starts by **reading** the request and **inferring** what it can. Only the genuinely ambiguous parts trigger a question.

## The Decision Loop

```
Read the request
  → Auto-detect: language, genre, mood, duration, theme
    → Anything missing? Ask 1–3 questions max
      → Build prompt formula
        → Structure lyrics
          → Call music_generate
            → Verify
              → Iterate or deliver
```

## First Response Defaults

Use these before asking follow-up questions:

- **Standard song request** -> infer language, genre, mood, and duration first.
- **User-provided lyrics** -> preserve the lyrics and add section tags.
- **Instrumental or jingle** -> default to instrumental mode immediately.
- **Vague style reference** -> treat the reference as a cue and infer the closest style family.
- **Image or URL input** -> enrich the request from the image or URL before questioning the user.

## Auto-Detect Cheat Sheet

| Signal | Detected from | Default if absent |
|---|---|---|
| Language | Words in the user's message | Same as conversation language |
| Genre | Adjectives ("epic", "romantic", "aggressive") and named references | Upbeat pop |
| Mood | Emotional cues in the request | Neutral positive |
| Duration | Explicit ("30 seconds", "8 minutes") | ~3 minutes |
| Theme | Nouns, verbs, named topics | Open — let the LLM pick |
| Vocal | "male voice", "female singer", "choir" | Solo vocal |
| Language of vocals | Same as user message | Same as user message |

## Question Patterns

### 1. Lyrics source

Trigger: user describes a song but does not provide lyrics and does not explicitly ask for instrumental.

Ask: **"Do you have lyrics, or should I write them?"**

Branches:
- User has lyrics → use them, add section tags
- User wants auto-lyrics → write them, structure them
- User wants instrumental → skip lyrics, set `instrumental: true` (provider-specific)

### 2. Vocal style

Trigger: user does not specify voice and the request is for a vocal track.

Ask: **"Any preference on voice — male, female, language, register?"**

Defaults: solo vocal, same language as user, mid register.

### 3. Instrumental vs vocals

Trigger: the request is a jingle, intro, or otherwise ambiguous about vocals.

Ask: **"Do you want vocals or instrumental only?"**

### 4. Reference artist or style

Trigger: user does not name an artist and the genre is broad.

Ask: **"Anything you want it to sound like — a specific artist, era, or reference track?"**

Skip this if the user already named a reference.

### 5. Energy level

Trigger: user says something vague like "make a song" or "a track about X".

Ask: **"Calm and intimate, or energetic and driving?"**

Default: medium energy.

### 6. Length

Trigger: user does not specify, and the use case is ambiguous.

Default: ~3 minutes. Only ask if the use case suggests a different length:

- jingle → 15–30s
- intro music → 30–60s
- background music for a video → ask the user for the video length
- epic / cinematic → 4–6 minutes

## Worked Examples

### Example 1: Clear request, no questions needed

> "Instrumental lofi for studying, no vocals."

Auto-detected:
- Genre: lofi
- Mood: calm, focused
- Duration: ~3 minutes (default)
- Vocal: none (instrumental)

Ask: nothing. Generate.

### Example 2: Vague, needs one question

> "Make me a song."

Auto-detected: nothing (literally nothing).

Ask: **"What kind of song — any genre, mood, language, or theme you have in mind? Or do you want me to surprise you?"**

If surprise: pick upbeat indie pop, EN, ~3 min, auto-lyrics. Confirm before generating.

### Example 3: Partial request, needs lyrics source

> "Una balada en español sobre el primer amor."

Auto-detected:
- Language: ES
- Genre: ballad
- Theme: first love
- Duration: ~3 minutes
- Mood: romantic (inferred)

Ask: **"Do you have lyrics, or should I write them in Spanish?"**

### Example 4: Full creative brief, no questions

> "Here's my poem. Turn it into a rock anthem with female vocals in Spanish, ~4 minutes."

Auto-detected:
- Lyrics: user-provided (the poem)
- Genre: rock anthem
- Vocal: female, Spanish
- Duration: ~4 minutes

Ask: nothing. Translate the poem into structured lyrics with section tags, build the prompt, generate.

### Example 5: Mashup or fast cloud cover

> "Take this Beyoncé track and turn it into reggaeton."

This is a cover / style transfer. Route by priority: use `music-craft-minimax`
for fast cloud cover, mashup, or advanced analysis; use ACE-Step in this skill
only if the user explicitly accepts a local, slower cover/repaint experiment.

Default response: **"That needs fast cover / style transfer from reference audio. Use `music-craft-minimax` for the cloud path, or I can try the slower local ACE-Step cover experiment if you prefer no cloud."**

## Edge Cases

### The user changes their mind mid-generation

If the user interrupts with a new direction after generation has started:

1. Stop the current iteration
2. Re-run auto-detect on the new request
3. Confirm the change before regenerating (a 1-line confirmation is enough)

### The user wants a 5-second variation on an existing track

This is not generation. It is editing. Point them to post-production tools.

### The user wants ten variations to choose from

Generate up to 3 variations on the same prompt, varying either the genre, the mood, or the structure (not all three at once). More than 3 is wasteful — narrow the creative space first.

### The user provides no request at all

Respond with the most neutral possible prompt and confirm before generating:

> "I will generate a 3-minute upbeat indie pop track in English with auto-generated lyrics about open roads. Confirm, or give me a direction."

### The user is in a non-English language

Auto-detect language from the user message. Use that language for the lyrics. The prompt formula in English can stay in English (most providers understand it) but if the user is in Spanish, consider also writing the prompt in Spanish for better vocal and stylistic alignment.

## Source-Audio Vocal and Length Checks

These are covered by the mandatory confirmations in [`input-workflows.md`](input-workflows.md):
- Vocal check: "Is this instrumental, or does it have vocals? If vocals, what language?"
- Length check: "Source is about <x>. Do you want same as source, 3:00, 3:30, or a specific length?"

They are targeted checks, not a new questionnaire.

## Tone of Questions

When asking, keep it short and concrete:

- ❌ "Would you like me to provide some lyrical content, or do you have specific verses, a chorus, or even just a thematic framework you would like me to develop further?"
- ✅ "Do you have lyrics, or should I write them?"

- ❌ "I want to make sure I understand the vocal character you envision. Should the vocal performance be delivered by a male or female performer, in what register, and in what language?"
- ✅ "Any preference on voice — male, female, language, register?"

If the user is in a hurry, prefer no questions at all over the right questions. Use the defaults.
