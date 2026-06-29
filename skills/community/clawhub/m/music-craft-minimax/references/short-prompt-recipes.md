# Short Prompt Recipes

MiniMax cloud generation is strongest for fast iteration when prompts are
compact. Keep standard `mmx music generate` prompts under about 500 characters
when possible. Put long production sheets in the local ACE-Step route.

Use the anti-sparse guard in every recipe: instruments keep playing, no
a cappella dropouts, no silent gaps.

## Indie Rock Ballad

```text
Indie rock ballad, 82 BPM, warm electric guitars, melodic bass, steady drums,
intimate lead vocal, bigger harmony choruses. Emotional but direct, natural
band performance. Anti-sparse: guitar, bass, drums, and vocal presence in every
section; no a cappella drops, no silent gaps.
```

## Synthwave

```text
Night-drive synthwave, 96 BPM, analog pads, arpeggiated bass, gated drums,
clear lead vocal, neon chorus lift. Polished 1980s texture, modern low end.
Anti-sparse: synths, bass, drums, and vocal energy stay active throughout.
```

## Trip-Hop

```text
Moody trip-hop, 78 BPM, dusty breakbeat, sub bass, muted guitar, smoky close
vocal, dark cinematic chorus. Keep it full and hypnotic. Anti-sparse: beat,
bass, texture, and vocal presence continue through every section.
```

## Bossa Nova Contrast

```text
Bossa nova reinterpretation, 92 BPM, nylon guitar, upright bass, brushed drums,
soft piano, relaxed bilingual-style vocal phrasing. Warm cafe mix. Anti-sparse:
rhythm section and harmony keep moving; no empty vocal-only sections.
```

## Heavy Post-Rock

```text
Heavy post-rock version, 84 BPM, tremolo guitars, huge live drums, distorted
bass, wide instrumental builds, restrained vocal in verses and explosive
choruses. Anti-sparse: full band bed remains active, no silent gaps.
```

## Practical Rules

- Inline references in the prompt, for example "in the spirit of Mogwai and
  Russian Circles", instead of relying on `--references` during batch work.
- If a prompt needs more than 500 characters, decide whether the local
  ACE-Step route is a better fit.
- If output duration must fit a hard slot, stop and use `music-craft` with
  ACE-Step.

