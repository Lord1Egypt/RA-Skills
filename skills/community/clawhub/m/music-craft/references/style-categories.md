# Style Categories

A quick reference for the 10 most-requested style categories, with their default instruments, BPM range, and mood. Use this when the user's request is broad (e.g., "make a song") and you need to pick a coherent default.

| Category | Instruments | BPM range | Default mood |
|----------|-------------|-----------|--------------|
| `french_chanson` | Accordion, upright bass, orchestral strings, piano, light percussion | 70–90 | Melancholic, romantic, dramatic |
| `rock` | Electric guitars, drums, bass, electric piano | 120–150 | Energetic, powerful, raw |
| `acoustic` | Acoustic guitar, light percussion, soft bass | 80–110 | Intimate, warm, organic |
| `epic_orchestral` | Full orchestra, choir, timpani, brass, French horn | 60–85 | Cinematic, grand, emotional |
| `jazz` | Piano, brass, double bass, drums, saxophone | 140–180 | Smooth, swing, sophisticated |
| `latin` | Acoustic guitar, congas, bongos, brass, claves | 90–130 | Warm, passionate, danceable |
| `pop` | Synths, drum machine, bass, electric guitar, handclaps | 100–130 | Catchy, upbeat, modern |
| `blues` | Electric guitar, harmonica, bass, drums, piano | 70–100 | Soulful, gritty, expressive |
| `electronic` | Synths, drum machines, bass drops, pads, arpeggiators | 110–140 | Atmospheric, pulsing, hypnotic |
| `ballad` | Piano, strings, light acoustic guitar, soft bass | 60–90 | Tender, emotional, slow |

## How to use this table

When the user is vague:

1. Pick the closest category to their request.
2. Take 3–5 instruments from the table.
3. Take the BPM range and pick a specific value (or omit if unsure).
4. Take 2–3 mood adjectives from the table.
5. Combine into a production-sheet prompt using the formula in [`references/prompt-formula.md`](prompt-formula.md).

### Worked example: vague request

User: "Make me a song."

Pick: `pop` (default for ambiguous), instruments = "synths, drum machine, bass, electric guitar, handclaps", BPM = 120, mood = "catchy, upbeat, modern".

Resulting prompt snippet:

```
Upbeat modern pop, catchy and feel-good mood, bright female vocal in English,
synths, drum machine, bass, electric guitar, handclaps,
ALL instruments always playing throughout, never drop to a cappella,
120 BPM in C major,
intro-verse-pre chorus-chorus-verse-chorus-bridge-chorus-outro,
modern radio mix, polished production quality,
AVOID sparse arrangements, AVOID minimalist sections
```

## When to override

The table is a default. Override when:

- The user names a specific sub-genre (e.g., "synth-pop", "drum and bass", "shoegaze") — use the sub-genre's specific instruments instead.
- The user names a reference artist — pull the artist's typical instruments and BPM.
- The user wants fusion — combine instruments from 2 categories (e.g., latin + electronic = "reggaeton").

## Sub-genre examples

| Sub-genre | Parent | Specific instruments and notes |
|-----------|--------|--------------------------------|
| `synth-pop` | pop | Analog synths, drum machine, gated reverb drums, bass synth; 110–130 BPM |
| `drum_and_bass` | electronic | Breakbeats, sub-bass, pads, vocal chops; 160–180 BPM |
| `shoegaze` | rock | Heavily distorted guitars, reverb-drenched vocals, dreamy textures; 100–130 BPM |
| `reggaeton` | latin + electronic | Dembow rhythm, 808 bass, synth pads, Spanish vocals; 90–100 BPM |
| `bossanova` | latin + jazz | Nylon guitar, light brushed drums, soft Portuguese vocals; 110–130 BPM |
| `k-pop` | pop | Bright synths, punchy 808s, layered harmonies, mixed-language lyrics; 110–130 BPM |
| `flamenco` | latin | Spanish guitar, palmas, cajón, passionate Spanish vocals; 100–180 BPM |
| `opera` | epic_orchestral | Full orchestra, choir, soprano/tenor solo, dramatic dynamics; 60–100 BPM |
| `lofi` | acoustic + electronic | Muted piano, vinyl crackle, mellow drums, soft bass; 70–90 BPM |
| `trap` | electronic | 808 hi-hats, sub-bass, sparse melody, rap vocals; 130–160 BPM (half-time feel) |
| `country` | acoustic | Steel guitar, fiddle, acoustic guitar, brushed drums, storytelling vocals; 90–130 BPM |
| `reggae` | latin | Offbeat guitar skanks, bass, drums, organ, Jamaican vocals; 60–90 BPM |
| `metal` | rock | Heavily distorted guitars, double bass drums, growled vocals; 140–200 BPM |
| `indie_pop` | pop | Jangly guitars, soft synths, breathy vocals, lo-fi touches; 110–125 BPM |
| `ambient` | electronic | Pads, drones, field recordings, no drums; 60–90 BPM |
| `funk` | jazz + electronic | Slap bass, wah guitar, tight drums, brass stabs; 95–115 BPM |
| `gospel` | ballad + epic_orchestral | Choir, organ, piano, call-and-response vocals; 80–120 BPM |
| `bluegrass` | acoustic | Banjo, fiddle, mandolin, upright bass, harmonies; 120–160 BPM |
| `salsa` | latin | Piano, congas, bongos, trumpets, timbales, Spanish vocals; 150–250 BPM |
| `dubstep` | electronic | Half-time drums, sub-bass drops, wobble bass; 140 BPM (half-time 70) |

These are not exhaustive — use them as anchors for prompt construction.

## Anti-Sparse Per Category

Some categories are more prone to sparse output than others. The high-risk ones (french_chanson, acoustic) need extra emphasis on the anti-sparse rules.

| Category | Sparse risk | Extra emphasis needed |
|---|---|---|
| `french_chanson` | 🔴 high | "quiet sections: reduced to accordion and bass only, still fully played" + "ALL instruments ALWAYS playing" |
| `ballad` | 🔴 high | "quiet sections: reduced to piano and bass only, still fully played" |
| `acoustic` | 🟠 medium | "fingerpicked guitar always present, soft percussion as constant texture" |
| `jazz` | 🟠 medium | "brass stabs and piano comping throughout, not just solo sections" |
| `epic_orchestral` | 🟢 low | Most providers handle this well; add "timpani rolls maintain energy" |
| `rock` | 🟢 low | "double-tracked guitars throughout" prevents drops |
| `electronic` | 🟢 low | "pad layers always sustaining" prevents gaps |
| `pop` | 🟢 low | Standard anti-sparse is usually enough |
| `blues` | 🟢 low | Standard anti-sparse is usually enough |
| `latin` | 🟢 low | Percussion tracks rarely go silent |

For the high-risk sub-genres not in the main table (ambient, lofi, drone), apply the same principle: explicit instruments and "all layers always playing" in the prompt.

See `SKILL.md` → Anti-Sparse Rules (Critical) for the canonical anti-sparse text.
