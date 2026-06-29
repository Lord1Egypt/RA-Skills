# Structure Tags

Lyrics for music generation are not free-form text. They are **timed sections** that the generator uses to shape the song. Every lyrics body should use section tags.

## Rules

- One tag per line, on its own line
- No descriptions inside brackets — anything in the brackets gets sung
- Blank line between sections
- Tags are case-insensitive but conventionally capitalized
- Use English tag names regardless of the song language

## Tag Safety Contract

Bracket tags are a strict contract with the generator. Some backends may sing
non-standard bracket text literally, so only use the whitelisted tags below
plus numbered variants such as `[Verse 2]` or `[Chorus 3]`.

Before spending a generation on provided or generated lyrics, run:

```bash
python3 scripts/lint_lyrics.py lyrics.txt --bpm 95 --target-seconds 180
```

If it reports invalid tags, fix the lyrics first. Do not use descriptive tags
such as `[Guitar Solo - distorted]`, `[Section 1]`, `[Lyrics]`, or
`[French vocals]`; put those instructions in the prompt, not in brackets.

## Tag Reference

### Core sections

| Tag | Effect | Typical duration |
|---|---|---|
| `[Intro]` | Opening section, often instrumental or sparse | 4–8s |
| `[Verse]` | Main verse, narrates the story | 16–24s |
| `[Pre Chorus]` | Build before the chorus | 8s |
| `[Chorus]` | Main hook, repeated 2–4 times in a song | 16–24s |
| `[Bridge]` | Contrast section, breaks the pattern | 8–16s |
| `[Outro]` | Closing section, often a chorus tail or fade | 8–16s |

### Connective tags

| Tag | Effect |
|---|---|
| `[Interlude]` | Short instrumental break between sections |
| `[Transition]` | Connective passage that bridges two sections |
| `[Post Chorus]` | Section immediately after the chorus (a hook, a phrase, an echo) |
| `[Hook]` | A short, catchy repeated motif — usually 1–2 lines |

### Dramatic effect tags

| Tag | Effect |
|---|---|
| `[Break]` | Dramatic pause of 1–2 seconds (silence or near-silence). Use between verse and chorus, or before the bridge, to create tension. |
| `[Build Up]` | Tension building before a drop or climax. Use before the first chorus and before the final chorus. |
| `[Inst]` | Pure instrumental section, no vocals |
| `[Solo]` | Instrument solo (typically guitar, synth, or sax) |

## Default Structure

If the user does not specify a structure, use this 8-section default that fits a ~3 minute pop or rock song:

```
[Intro]
[Break]
[Verse]
[Pre Chorus]
[Chorus]
[Verse]
[Pre Chorus]
[Chorus]
[Bridge]
[Chorus]
[Outro]
```

For shorter tracks (jingles, intros, under 60 seconds), compress to:

```
[Intro]
[Verse]
[Chorus]
[Outro]
```

## Worked Lyrics Example

```
[Intro]

[Break]

[Verse]
I walked alone beneath the rain
Every window knew my pain

[Pre Chorus]
And the city held its breath tonight

[Build Up]

[Chorus]
I'm still here, I'm still yours
Even when the world ignores

[Break]

[Verse]
You said love was just a word
But I heard everything you heard

[Pre Chorus]
And the city held its breath tonight

[Chorus]
I'm still here, I'm still yours
Even when the world ignores

[Bridge]
Let the silence speak for us
Let the dark become a friend

[Build Up]

[Chorus]
I'm still here, I'm still yours
Even when the world ignoooores

[Outro]
I'm still heeeeere
```

## Lyrics from ASR (Whisper)

If lyrics are extracted from audio with Whisper or another ASR system, treat the transcript as **unverified** until it passes sanity checks:

- Prefer Whisper `medium` for lyrics extraction. Use `small` only for quick drafts.
- Use `large-v2` for complex singing, noisy audio, or multilingual vocals.
- If the `whisper` CLI exists but `python3 -c "import whisper"` fails, use the
  Python interpreter from the CLI shebang instead of assuming the active shell
  Python has the package installed.
- Cross-check with web lyrics or user-provided lyrics when possible.
- Strip transcript-only markers such as `[Section N]`, timestamps, ASR labels,
  and repeated machine-generated headings before final generation.
- Normalize unclear section markers to the canonical tag set unless a more
  specific tag is musically necessary.
- Flag language mismatches, very short looping transcripts, and transcript themes that conflict with the known song/user context.
- Do not build final prompts around suspicious lyrics without asking the user or rerunning extraction with a stronger model.

Full cleanup recipe: [`lyrics-cleanup.md`](lyrics-cleanup.md).

## Vocal Effects Through Lyrics

Music generators do not have a "vocal speed" parameter. Achieve effects through lyrics formatting.

### Elongation (held notes)

Stretch key vowels:

- `toooooou`
- `rieeeeen`
- `aveeeec`
- `I caaan't goooo on`

### Fewer syllables for stretching

Instead of: `I cannot continue with you anymore`
Use: `I caaan't gooo on with yoooou`

This gives the model room to stretch the line.

### Repetition with escalation

For a chorus that builds:

```
[Chorus]
I'm still here, I'm still yours
I'm still here, I'm still yours
I'm still heeeere, I'm still yooouuurs
I'm still heeeere, I'm still yooouuurs
```

## Emotion-Specific Lyrics Patterns

The elongation techniques above combine into patterns that evoke specific emotions. Use these as anchors when the user wants a song that sounds a particular way.

### Desperation (high effort, falling intonation)

```
[Verse]
I caaaan't goooo on with yoooou
Nooooo, pleaseeee, don't leeeave

[Pre Chorus]
Don't youuuu, don't youuuu, don't youuuu goooo

[Chorus]
I'm beggiiiiiing, I'm beggiiiiiing
Stay with meeeee
```

Long vowels, descending pattern, high repetition.

### Joy (bright, energetic)

```
[Verse]
Sun is shiiiiining
And I'm feeliiiiing fine

[Chorus]
Oh oh oh! Yeah yeah yeah!
This is my dayyy!
```

Short syllables, exclamations, rising pattern.

### Melancholy (breathy, slow)

```
[Verse]
Stil hereee...
Waiting for yoooou...

[Break]

[Verse]
Counting the days
That weee looost

[Chorus]
I miss yoooou... stil...
Every night...
```

Long vowels with trailing decay, lots of `[Break]`, low energy throughout.

### Vulnerability (whispered, intimate)

```
[Verse]
I... don't... knoooow...
If i... caaaan...

[Pre Chorus]
I thought i was strooong
But i'm... not...

[Chorus]
I need yoooou... please...
Don't let me gooo
```

Stretched with hesitation (use `...` to indicate pauses), first person, intimate.

### Triumph (powerful, building)

```
[Verse]
We were broken
We were down

[Pre Chorus]
But we stood up
We held our ground

[Build Up]

[Chorus]
WE WILL RISE
WE WILL FIGHT
THIS IS OUR NIGHT
```

Short, punchy, declamatory. Capital letters (model often interprets as shouted).

### Yearning (high, sustained)

```
[Verse]
Where are yoooou...
Where have yoooou goooone...

[Pre Chorus]
Do youuuu think of meee
When the niiight is looong

[Chorus]
I'm waitiiiiing... for yoooou...
To come hoooome
```

Long vowels, ascending, with pauses.

### Anger (shouted, sharp)

```
[Verse]
Enough is enough
No more lies

[Pre Chorus]
You think you can break me
You think you can win

[Chorus]
NO! NO! NO!
I won't take this anymore!
GET OUT!
```

Short, exclamatory, capital letters. The model often interprets ALL CAPS as shouted delivery.

### Confidence (clear, direct)

```
[Verse]
I am the storm
I am the fire

[Pre Chorus]
I know what I want
I know who I am

[Chorus]
I will rise
I will fight
I will win
```

Short declarative phrases, periods for finality, no hesitation.

### Hopeful (bright, rising, ascending)

```
[Verse]
I see it now
The light is breaking through

[Pre Chorus]
Maybe tomorrow
Maybe today
Maybe this moment

[Build Up]

[Chorus]
I believe I believe I believe
We will rise
We will fly
We will find our way
```

Future tense, ascending intonations, building repetition.

### Tragic (doomed, resigned, falling)

```
[Verse]
The stars have aligned against us
As they always would

[Pre Chorus]
I tried to fight it
I tried to hold on

[Chorus]
This is the end
This was always the end
I see it now
I see it now
```

Acceptance language, falling inflections, past tense.

### Heroic (powerful, march rhythm)

```
[Verse]
We march to the sound of the drums
Our banners high in the morning light

[Pre Chorus]
They said we'd never stand a chance
They said we'd fall

[Build Up]

[Chorus]
WE STAND
WE FIGHT
WE RISE
FOR HONOR
FOR GLORY
FOR US
```

Declarations, march rhythm, building repetition.

### Tender (warm, gentle, stable, affectionate)

```
[Verse]
Stay with me
Just a little longer
The night is young

[Pre Chorus]
I feel your hand in mine
Your breath against my skin

[Chorus]
I'm holding youuu
I'm holding yoooou
Never let me go
```

Soft language, first person, gentle, no exclamation.

### Sensual (breathy, low register, sustained)

```
[Verse]
Your voice is a whisper
Against my skin

[Pre Chorus]
Closer now
Closer still

[Chorus]
Don't stop don't stop
I'm not ready to let goooo
Tonight tonight tonight
Is ours
```

Physical/romantic imagery, slow delivery, long vowels, low register.

### Lonely (breathy, single voice, isolated)

```
[Verse]
I'm sitting here
In this empty room
No one to talk to
No one to call

[Break]

[Verse]
The silence is deafening
The night is long

[Chorus]
I'm alone
I'm alone
Does anyone hear me
Does anyone care
```

Isolation language, first person, long pauses, single voice (no harmony).

### Playful (bright, bouncy, fun)

```
[Verse]
Hey hey hey
What's the time
It's party time

[Pre Chorus]
Dancing on the table
Dancing on the chair
Dancing everywhere

[Chorus]
YEAH YEAH YEAH
We don't care
YEAH YEAH YEAH
We're not going anywhere
```

Fun language, short syllables, exclamations.

### Haunting (breathy, dissonant, sparse, dark)

```
[Verse]
The walls are closing in
I hear the whispers in the dark

[Pre Chorus]
Something is here
Something is watching

[Chorus]
Stay with me
Don't let go
The night is looong
And I am alone
```

Eerie imagery, slow, deliberate, long pauses.

### Serene (very soft, stable, peaceful, no peaks)

```
[Verse]
The water is still
The wind is soft

[Break]

[Verse]
The sky is clear
The air is cool

[Chorus]
Breathe... breathe...
Let it go... let it go...
All is well... all is well...
```

Nature/peace imagery, very few words, long pauses.

### Celebratory (bright, building, declarative, joyful)

```
[Verse]
The night is young
And we are together

[Pre Chorus]
Raise your hands
Raise your voice
Raise your heart

[Build Up]

[Chorus]
CELEBRATE! CELEBRATE!
Tonight is ours!
CELEBRATE! CELEBRATE!
We are alive!
```

Togetherness language, exclamations, building repetition.

### Bittersweet (mixed bright and dim)

```
[Verse]  (bright, joyful delivery)
The sun is shiiining
The birds are siiinging
It was the best day of my life

[Pre Chorus]  (transitioning)

[Chorus]  (dim, melancholic delivery)
And now it's over
And now you're gone
And I'm still here... alone
```

Juxtaposition: happy language with sad imagery, or vice versa. Mixed tenses.

### When to Use Each Pattern

Match the lyrics pattern to the target emotion AND the prompt wording. The prompt, lyrics, and arrangement should all point at the same emotion.

| Target emotion | Lyrics pattern | Match with prompt | Match with arrangement |
|---|---|---|---|
| Desperation | Long stretched vowels, descending | strained, raw, falling | sparse piano + dramatic strings |
| Joy | Short repeated, exclamations | bright, energetic, smiling | dense pop, hand claps |
| Melancholy | Trailing decay, pauses | breathy, low, slow | sparse piano + strings |
| Vulnerability | Stretched with hesitation | whispered, fragile | single instrument + voice |
| Triumph | Short, declamatory, capitals | powerful, building | full band, choir in climax |
| Yearning | Long vowels, ascending | breathy, high, sustained | pads, high register |
| Anger | Short, exclamatory, capitals | aggressive, shouted, sharp | distorted, punchy |
| Confidence | Short declarative, periods | strong, clear, stable | driving, full band |
| Hope | Future tense, ascending, building repetition | bright, rising, optimistic | building, light to dense |
| Tragic | Acceptance, falling, past tense | doomed, resigned, falling | no climax, restrained |
| Heroic | Declarations, march rhythm, building | powerful, march, building | full orchestra, brass, timpani |
| Tender | Soft, first person, no exclamation | warm, gentle, stable | soft piano + guitar |
| Sensual | Physical imagery, long vowels, low register | breathy, low, sustained | R&B, low register pads |
| Lonely | Isolation, first person, pauses, single voice | breathy, isolated, falling | single instrument, sparse |
| Playful | Fun language, short syllables, exclamations | bright, bouncy, fun | syncopated, light instruments |
| Haunting | Eerie imagery, long pauses | breathy, low, dark | dissonant, sparse, low pads |
| Serene | Nature/peace, very few words, long pauses | soft, stable, slow | ambient, no percussion |
| Celebratory | Togetherness, exclamations, building | bright, building, joyful | full band, horns, choir |
| Bittersweet | Juxtaposition, mixed tenses | bright verses + dim chorus (or vice versa) | bright verse + dim chorus arrangements |

For the full emotion recipes (with arrangement + section structure), see [`../music-craft-minimax/references/emotion-delivery.md`](../../music-craft-minimax/references/emotion-delivery.md).

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| `chorus:` (lowercase) | Some generators are strict | Use `[Chorus]` |
| `[Verse 1 - slow]` | The description inside brackets gets sung | Use just `[Verse]` |
| No blank line between sections | Generator may merge them | Always blank line |
| `[Intro] [Verse]` on the same line | Same as above | One tag per line |
| Missing `[Break]` before a big drop | The drop feels rushed | Add `[Break]` 1–2s before the chorus |
| Forgetting the `[Outro]` | Song ends abruptly | Always close with `[Outro]` |

## Multi-Language Tags

Tags stay in English. The song text inside each section is in whatever language the user requested. Example (Spanish song):

```
[Intro]

[Verse]
Caminé solo bajo la lluvia
Cada ventana conocía mi dolor

[Pre Chorus]
Y la ciudad contuvo el aliento esta noche

[Chorus]
Sigo aquí, sigo siendo tuyo
Incluso cuando el mundo me ignora

[Bridge]
Que el silencio hable por nosotros
Que la oscuridad se vuelva amiga

[Outro]
Sigo aquiiiii
```

This is correct and portable across providers.
