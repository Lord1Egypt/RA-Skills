# Examples

Use `music-craft` when the user wants a new song built from text, style, or descriptive inputs rather than audio-based transformation.

For prompt shape details, see [`prompt-formula.md`](./prompt-formula.md) and [`input-workflows.md`](./input-workflows.md).

## Routing Table (Cheat Sheet)

| Example | Use this skill because | First response/questions | Prompt shape |
|---|---|---|---|
| Standard song | The user wants an original song from a style brief, not a cover or mashup. | Infer genre, mood, language, and duration first; ask only for missing lyrics source or vocal type. | `genre + mood + voice + instruments + anti-sparse + BPM/key + structure + avoid list` |
| User-provided lyrics | The user already has lyrics and wants them turned into a finished track. | Preserve the lyric text; ask only for missing target style, voice, or length details. | `style brief + supplied lyrics + section tags + production notes` |
| Instrumental / jingle | The user wants a short non-vocal cue, sting, bumper, or ad jingle. | Set instrumental mode immediately; ask duration only if the use case does not imply it. | `instrumental only + short form + hooky motif + no vocals` |
| Text-only style reference | The user names a song, era, or genre as a vibe reference but provides no audio. | Translate the reference into descriptors; ask only which aspect matters if the reference is broad. | `style reference translated into descriptors, not a literal rewrite` |
| Image or URL vibe enrichment | The user gives an image or webpage and wants the music to match that mood. | Analyze or fetch first; ask only about remaining ambiguity after extracting cues. | `extract vibe cues first, then map them to genre, mood, and instruments` |
| Linter catch: missing lyrics source + vague instrumentation | The user says "make it emotional and cinematic" but does not say whether to write lyrics or what instruments to use. | Ask whether the track should have auto-lyrics or supplied lyrics, then replace vague words with concrete instruments and a mode. | `missing lyrics_source + explicit instruments + anti-sparse + structure` |

## Worked Examples

Each example shows the same flow: **intake → prompt → verification**. Keep the structure short so future agents copy the shape, not the exact prose.

### Example 1: Spanish Pop Song

**Request:** "Quiero una pop alegre en español sobre el verano, unos 3 minutos."

**Intake:**

```
clear:     language=es, genre=pop, theme=summer, duration=~3min
inferred:  mood=feel_good, vocal_mode=solo_female, structure=standard
missing:   lyrics_source
```

**First question:** "Do you have lyrics, or should I write them in Spanish?"

**Final prompt (auto-lyrics branch):**

```
Upbeat summer pop, feel-good optimistic mood, bright female vocal in Spanish,
electric guitar, synthesizers, drum machine, bass guitar, handclaps, maracas,
ALL instruments always playing throughout, never drop to a cappella,
120 BPM in C major,
intro-verse-pre chorus-chorus-verse-chorus-bridge-chorus-outro structure with catchy pre-chorus build,
modern radio mix, polished production quality,
AVOID sparse arrangements, AVOID minimalist sections, AVOID dark or moody tones
```

**Verification checklist:**

- [ ] Language: Spanish vocals throughout
- [ ] Vocal mode: female solo vocal present
- [ ] Section structure: 7+ distinct sections
- [ ] Duration: ~3 minutes
- [ ] Genre: recognizably pop, not generic acoustic
- [ ] Mood: bright, summery, not melancholic

### Example 2: English Instrumental Jingle

**Request:** "I need a 30-second lofi jingle for a YouTube intro, no vocals."

**Intake:**

```
clear:     language=instrumental, genre=lofi, duration=30s, vocal_mode=instrumental
inferred:  mood=chill_focused, structure=loop
missing:   (none — go directly to prompt)
```

**First question:** none.

**Final prompt:**

```
Instrumental only, no vocals, no lyrics. Lofi hip-hop, chill and focused,
lofi drum machine, vinyl crackle, soft piano chords, mellow bass, jazzy Rhodes,
ALL elements always playing, never drop to silence,
75 BPM in F minor,
short looping structure (intro-loop-outro ~30s),
soft low-pass mix, warm tape saturation,
AVOID vocals, AVOID bright synths, AVOID high-energy drums
```

**Verification checklist:**

- [ ] No vocals anywhere
- [ ] Duration: ~30s, not 3 minutes
- [ ] Genre: lofi, with vinyl crackle / piano / Rhodes signature
- [ ] Mood: chill, suitable for studying
- [ ] Loops cleanly without a harsh ending
- [ ] Mood words ("chill", "focused") are grounded in the production details above

### Example 3: User-Provided Lyrics

**Request:** "Here's a poem I wrote. Turn it into a rock anthem with female vocals in Spanish, ~4 minutes."

**Intake:**

```
clear:     lyrics_source=user_provided, language=es, genre=rock_anthem,
           vocal_mode=solo_female, duration=~4min
inferred:  mood=epic, structure=anthem_shape
missing:   (none)
```

**First question:** none — everything is clear.

**Final prompt:**

```
Epic Spanish rock anthem, triumphant emotional mood, powerful female vocal in Spanish,
electric guitar (lead and rhythm), bass, drums, orchestral strings, piano,
ALL instruments always playing, never a cappella or silent,
128 BPM in E major,
intro-verse-pre chorus-chorus-verse-pre chorus-chorus-bridge-break-chorus-outro structure with anthemic build,
wide dynamic contrast, building intensity to explosive final chorus,
full production, stadium mix quality,
AVOID sparse, AVOID a cappella, AVOID minimalist
```

**Lyrics body (structured, user's words preserved, only section tags added):**

```
[Intro]

[Verse 1]
[user's original lines, untouched]

[Pre Chorus]
[user's original lines, untouched]

[Chorus]
[user's original lines, untouched]

[Verse 2]
[user's original lines, untouched]

[Pre Chorus]
[user's original lines, untouched]

[Chorus]
[user's original lines, untouched]

[Bridge]
[user's original lines, untouched]

[Break]

[Chorus]
[user's original lines, untouched]

[Outro]
```

**Verification checklist:**

- [ ] Lyrics: user's words appear verbatim, only section tags added
- [ ] Language: Spanish vocals
- [ ] Vocal mode: female solo
- [ ] Section structure: anthem shape with bridge and final chorus
- [ ] Duration: ~4 minutes
- [ ] Genre: rock anthem, with electric guitars and strings

### Example 4: Image-Inspired Track

**Request:** "Turn this album art into a song." (User attaches neon synthwave artwork)

**Intake:**

```
clear:     reference=image (neon palette, retro typography, 80s car)
inferred:  genre=synthwave_retro, mood=dark_nostalgic, language=conversation_default,
           duration=~3min, structure=standard
missing:   lyrics_source, vocal_mode
```

**First response (enrich first):** Run `image` analysis on the artwork. Extract: neon pink/cyan palette, 1980s aesthetic, dark undertones, retro car. Map to synthwave subgenre.

**First question (after enrichment):** "Synthwave with a dark retro feel. Do you have lyrics, or should I write them?"

**Final prompt (auto-lyrics branch):**

```
Retro synthwave, dark nostalgic mood, moody male vocal in English,
analog synthesizer pad, arpeggiated synth lead, drum machine, reverb-heavy electric piano, bass synth,
ALL elements always playing, never drop to silence,
98 BPM in A minor,
intro-verse-chorus-verse-chorus-bridge-chorus-outro structure with retro 80s arpeggios,
gated reverb on drums, wide stereo synth mix, neon-noir atmosphere,
AVOID acoustic instruments, AVOID bright pop tones, AVOID modern trap drums
```

**Verification checklist:**

- [ ] Genre: synthwave with retro 80s signatures (arpeggios, gated reverb)
- [ ] Mood: dark nostalgic, not bright
- [ ] Language: English vocals
- [ ] Section structure: 7+ sections
- [ ] Atmosphere: matches the image's neon-noir vibe
- [ ] No acoustic instruments in the output

### Example 5: Text-Only Style Reference

**Request:** "Make a song like 'Bohemian Rhapsody'."

**Intake:**

```
clear:     reference=bohemian_rhapsody
inferred:  genre=rock_opera, mood=dramatic, language=en,
           structure=multi_section, duration=~6min
missing:   lyrics_source
```

**First response (enrich if needed):** `web_search` "Bohemian Rhapsody structure analysis" for richer context, then translate into descriptors. Do not paste copyrighted lyrics.

**First question:** "Anything from 'Bohemian Rhapsody' you want me to lean on — operatic vocals, multi-section structure, dramatic dynamics, or all of it?"

**Final prompt (full-reference branch):**

```
Operatic rock ballad, dramatic theatrical mood, dynamic multi-vocal performance in English
(male lead, choir, layered harmonies, occasional a cappella break in the opera section only),
piano, electric guitar, bass, drums, orchestral strings, choir,
ALL instruments and voices playing whenever their section calls for them,
72 BPM shifting to 120 BPM and back across the song,
intro-ballad-verse-pre chorus-operatic-section-verse-pre chorus-operatic-section-bridge-operatic-section-coda-outro,
extreme dynamic contrast — quiet intimate piano intro, building to thunderous operatic climax,
studio production, multi-layered mix,
AVOID minimalist sections except the explicit opera break, AVOID monotone energy throughout
```

**Verification checklist:**

- [ ] Genre: operatic rock, not generic ballad
- [ ] Multi-section structure: ballad → operatic section → bridge → coda
- [ ] Tempo: shifts from slow ballad to faster operatic
- [ ] Multiple vocal layers present
- [ ] Dynamic contrast: quiet intro building to loud climax
- [ ] Duration: ~6 minutes, not 3

## Notes

- This skill is the right choice when the input is mostly descriptive.
- If the user provides audio and wants the original melody preserved, route to the MiniMax skill instead.
- If available, use [`../../music-craft-minimax/scripts/lint_music_request.py`](../../music-craft-minimax/scripts/lint_music_request.py) as a quick routing and prompt-lint helper before generation. The linter catches missing required slots and conflicting language signals, but does not enforce mood grounding — verify that manually.
