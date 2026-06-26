# Seedance × Logo Motion Design

Specialist playbook for **logo animations** — brand reveals, intros, bumpers, stings — built on Seedance 2. Use this when the user provides a logo (PNG/SVG export/product screenshot) and wants a polished motion-design sequence.

The pixcli API auto-detects this case and swaps in a dedicated Motion Logo Director prompt when:

1. A start image is attached (`--from logo.png`), AND
2. The prompt mentions **logo / brand / wordmark / emblem**, AND
3. The prompt mentions motion intent (**animate / motion / reveal / intro / bumper / sting / opener / title card**).

When those three hit, the enricher outputs a 1000–1500 character director brief in the format below. Otherwise it falls back to the standard Seedance formula in `seedance-playbook.md`.

---

## When to use this

| Yes | No |
|-----|----|
| "Animate this logo" + `--from logo.png` | "A woman walking in the rain" (no logo context) |
| "15s brand reveal for FlowPilot" + `--from logo.png` | Product shot animation (use standard Seedance formula) |
| "Morphing intro bumper that reveals our logo at the end" | Character animation (use i2v formula) |

---

## The Motion Logo Director output structure

The enricher will always emit a prompt with these sections, in this order:

```
Ultra-sleek minimal motion design sequence. [Background]. [Material & lighting]. [Overall style].
Locked-off static center frame, no cuts, no camera movement. All motion is smooth and mathematical.

0–2s  [STATE A → STATE B]: [chaotic elements snap/coalesce into first organized shape]
2–4s  [STATE B → STATE C]: [first shape compresses/melts into a core feature shape]
4–7s  [STATE C → STATE D]: [second form wraps/weaves into a complex geometric structure]
7–10s [STATE D → STATE E]: [complex structure flattens/spins/fractures into a dynamic pattern]
10–12s [STATE E → PRE-LOGO]: [pattern snaps into an arrangement hinting at the logo]
12–13s [HOLD]: the structure holds for one silent beat
13–15s [LOGO]: morphs seamlessly into the minimalist brand logo: "[Brand Name]"

Sound Design: [audio arc — cues tied to visual moments]
Music: [style, tempo, instruments, emotional arc]
Style: [chosen aesthetic references]. Mood: [3–4 keywords].
```

**Six stages, five distinct morphing transitions, one 1-second hold before the reveal.**

---

## The four aesthetic modes

The director picks ONE based on the product/brand:

| Mode | Keywords | Best for |
|------|----------|----------|
| **Apple Cupertino** | Deep titanium or space-black background, frosted glass (glassmorphism), soft specular highlights, premium ambient lighting | Flagship hardware, premium AI tools, minimalist tech |
| **Microsoft Fluent** | Soft layered environments, acrylic translucent textures, playful geometric structure, directional studio lighting | Productivity software, collaboration tools, ecosystems |
| **Bauhaus / Kenya Hara** | Soft off-white background, deep carbon-black elements, matte e-ink texture, no glow, flat architectural minimalism | Efficiency tools, readers, minimalist content platforms |
| **Vercel / Linear** | Pure void black, sharp glowing accent lines (neon blue/purple), wireframes, high-tech grids | Developer tools, frameworks, high-performance compute |

---

## The transition verb palette

**Every stage must morph INTO the next.** Nothing appears or disappears from nothing. Use a DIFFERENT verb in each stage — repetition dulls the sequence.

- `snaps magnetically into`
- `melts together into`
- `wraps around itself into`
- `flattens instantly into`
- `compresses inward into`
- `fractures into`
- `spirals into`
- `dissolves into`
- `crystallizes into`
- `unfolds into`

---

## Rhythm — never uniform

Vary stage durations across the clip. A musical rhythm feels dynamic:

- 15s clip: `2 / 2 / 3 / 3 / 3 / 2` (6 stages)
- 10s clip: `2 / 2 / 2 / 2 / 1 / 1` (6 stages — shorter hold)
- 8s clip: compress to 5 stages: `2 / 2 / 2 / 1 / 1`

Faster stages (2s) create energy. Slightly longer stages (3s) let complex morphs breathe.

---

## Recipe — "Animate this logo"

```bash
pixcli video "Generate a 15-second minimal motion design reveal for our brand FlowPilot. \
Use the Apple Cupertino aesthetic. Include voiceover: 'Out of noise, clarity.'" \
  --from flowpilot-logo.png \
  -m seedance-2-i2v \
  -d 15 \
  -r 16:9 \
  -q high \
  -o flowpilot-reveal.mp4
```

The API:
1. Detects `logo` + `reveal` + start image → swaps to Motion Logo Director prompt.
2. Sees the attached logo via vision and locks the final beat to morph into it.
3. Picks the Apple Cupertino style you requested (or auto-picks if you don't specify).
4. Emits a 6-stage timeline with voiceover embedded in stages 2-4s and 7-10s.

---

## Recipe — Dev-tool intro bumper

```bash
pixcli video "8-second opener bumper for our dev tool Pinzas. \
Vercel/Linear aesthetic with glowing neon-purple wireframe grids. \
Ends on our logo." \
  --from pinzas-logo.png \
  -m seedance-2-i2v \
  -d 8 \
  -r 16:9 \
  -o pinzas-bumper.mp4
```

---

## Recipe — B2B SaaS reveal (Microsoft Fluent)

```bash
pixcli video "15-second animated logo reveal intro for ClarityOps. \
Microsoft Fluent aesthetic, soft layered acrylic gradients, playful structural geometry. \
Voiceover: 'Operations, on your side.'" \
  --from clarityops-logo.svg.png \
  -m seedance-2-i2v \
  -d 15 \
  -r 16:9 \
  -q high \
  -o clarityops-intro.mp4
```

---

## What NOT to do

- **Don't** stuff animation adjectives into a short prompt and skip the logo image. Without `--from`, the Motion Logo Director mode will not activate and you'll get generic Seedance output.
- **Don't** add multiple camera moves. The format is **locked-off static center frame**. Period.
- **Don't** request more than 6 stages — Seedance loses coherence past 6 beats.
- **Don't** mix aesthetic modes. Pick one and commit. "Apple Cupertino meets Vercel" reads as conflicting instructions.
- **Don't** skip the pre-logo HOLD. The 1-second silent beat is what makes the reveal land.

---

## Sound design guidance

The enricher emits a `Sound Design:` paragraph tied to specific visual moments. Typical audio cues:

| Visual beat | Sound cue |
|-------------|-----------|
| Chaotic elements snapping into grid | Crisp mechanical clicks, UI-snap ticks |
| Fluid melt / wrap | Smooth liquid swooshes, soft reverberated sweeps |
| Spiral / fracture | Rising harmonic whoosh, glassy shatter tail |
| Pre-logo HOLD | Brief silence — or a single low sub-drop |
| Logo reveal | Soft piano note, warm synth pad, or brand sting |

If you want pixcli to generate these sounds separately, use `pixcli sfx` per cue and composite in Remotion. The native Seedance `--audio` flag can render plausible ambient audio inline for fast iteration.

---

## Music arc

The `Music:` line describes background music style, tempo, instruments, and emotional arc. Keep it 1–2 sentences. Example outputs:

- *"Minimal ambient piano with a slow-rising synth pad, starts sparse and introspective, crescendos into a single held chord at the logo reveal."*
- *"Driving electronic pulse at 110 bpm, filtered kick and glassy arpeggios, builds tension across the chaos beats and resolves clean on the wordmark."*

---

## Voiceover placement

If the user requests voiceover, the director **embeds lines inline** at the appropriate timeline stages — NOT as a separate block. Typical placement:

- One line at 2–4s (hook / problem framing)
- One line at 7–10s (value statement)
- Brand name at 13–15s on the logo reveal

Voice tone is specified in the first occurrence (e.g., "Calm, crisp male voice.").

To actually render the voiceover, generate it separately with `pixcli voice` and layer it in Remotion — Seedance audio is atmospheric, not spoken word.

---

## Cheat sheet

| I want… | Flags |
|---------|-------|
| 15s Apple-style logo reveal | `--from logo.png -m seedance-2-i2v -d 15 -q high` + say "Apple Cupertino" in the prompt |
| Dev-tool bumper | mention "Vercel aesthetic" + `--from logo.png -d 8` |
| B2B intro with voiceover | mention "Microsoft Fluent" + include voiceover line in the prompt |
| Minimalist brand reveal | mention "Kenya Hara / Bauhaus" + `-q high` |
| Quick draft | swap to `-q draft` — routes to cheaper 480p Seedance |

---

**See also:** `seedance-playbook.md` for standard (non-logo) video prompting, `prompt-cookbook.md` for ready-to-paste recipes.
